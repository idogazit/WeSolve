<template>
    <div class="bg-transparent">
        <ul class="list-group list-group-horizontal-sm">
            <li class="bg-transparent list-group-item border-0 .flex-fill pr-1 pl-1 pd-3" v-for="topic in topicList" :key="topic"><span class="badge badge-danger topic-label-tag">{{ topic["topicName"] }} [{{topic["count_votes"]}}]</span></li>
            <li class="bg-transparent list-group-item border-0 .flex-fill pr-1 pl-1 pd-3" v-for="label in labelList" :key="label"><span class="badge badge-warning topic-label-tag">{{ label["labelName"] }}: {{ label["labelValue"] }}</span></li>
            <li v-if="showForm == false" class="bg-transparent list-group-item border-0 .flex-fill pr-1 pl-1 pd-3">
                <button class="btn btn-default m-0 p-0" data-bs-toggle="tooltip" data-bs-placement="top" title="Add Label or Topic">
                    <img @click="enableShowForm" class="plus" src="https://img.icons8.com/external-tanah-basah-glyph-tanah-basah/48/26e07f/external-plus-essentials-tanah-basah-glyph-tanah-basah-2.png" />
                </button>
            </li>
        </ul>
        <div v-if="showForm" class="container">
          <div class="form-group m-2">
          </div>
            <form id="topic-form" class="form-inline" @submit.prevent="onTopicSubmit">
                <div class="form-group m-2">
                    <label>Add Topic:</label>
                </div>
                <div class="form-group">
                  <SearchAutocomplete :items="getAllTopics" v-model="selectedTopicName" @onChange="onChange"/>
                </div>
                <div class="form-group m-2">
                    <button
                        type="submit"
                        class="btn btn-success btn-sm"
                        >Submit Topic
                    </button>
                    <button class="btn btn-default ml-2 p-0" data-bs-toggle="tooltip" data-bs-placement="top" title="Topic votes are accumulated! Adding a topic vote will affect the topic significance of the question">
                      <img class="info" src="https://img.icons8.com/fluency/48/000000/info.png"/>
                    </button>
                    <button class="btn btn-default m-0 p-0">
                        <img class="m-2" @click="disableShowForm" id="close2" src="https://img.icons8.com/flat-round/64/26e07f/delete-sign.png" />
                    </button>
                </div>
            </form>

            <form id="label-form" class="form-inline" @submit.prevent="onLabelSubmit">
                <div class="form-group m-2">
                    <label>Add Label:</label>
                </div>
                <div class="form-group">
                    <select v-model="selectedLabelName">
                        <option disabled selected id="defaultLabelName" :value="''">Select Label</option>
                        <option v-for="label in allLabels.results" :key="label">{{ label["labelName"] }}</option>
                    </select>
                </div>
                <div class="form-group">
                    <select v-model="selectedLabelValue">
                        <option disabled selected id="defaultLabelValue" :value="''">Select Label Value</option>
                        <option v-for="labelValue in getLabelValues" :key="labelValue">{{ labelValue }}</option>
                    </select>
                </div>
                <div class="form-group m-2">
                    <button
                        type="submit"
                        class="btn btn-success btn-sm"
                        >Submit Label
                    </button>
                    <button class="btn btn-default m-0 p-0">
                        <img class="m-2" @click="disableShowForm" id="close" src="https://img.icons8.com/flat-round/64/26e07f/delete-sign.png" />
                    </button>
                </div>
            </form>


        </div>
    </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import SearchAutocomplete from "@/components/SearchAutocomplete";
export default {
    components: {
      SearchAutocomplete
    },
    props: {
        questionId: {
            type: String,
            required: true
        }
    },
    data() {
        return {
          questionLabels: [],
          questionTopics: [],
          allLabels: [],
          allTopics: [],
          selectedLabelName: "",
          selectedLabelValue: "",
          selectedTopicName: "",
          showForm: false,
          topicList: [],
          labelList: [],
        }
    },
    computed: {
        getLabelValues() {
            var labelValues;
            this.allLabels.results.forEach((result) => {
                if (result.labelName === this.selectedLabelName) {
                labelValues = result.possibleValues;
                }
            });
            return labelValues;
        },
        getTopics() {
            return this.questionTopics.results;
        },
        getLabels() {
            return this.questionLabels.results;
        },
        getAllTopics() {
          const allTopicsList = [];
          this.allTopics.results.forEach((result) => {
              allTopicsList.push(result["topicName"]);
          });
          return allTopicsList;
        },
    },
    methods: {
        enableShowForm() {
            this.showForm = true
        },
        disableShowForm() {
            this.showForm = false
        },
        getLabelsTopics() {
            let endpoint = `/api/questions/${ this.questionId }/labels/`;
              apiService(endpoint)
                  .then(data => {
                    if (data) {
                      this.questionLabels = data;
                      this.questionLabels.results.forEach((result) => {
                        if (result["count_votes"] >= 3) {
                          this.labelList.push(result);
                        }
                      });
                    }
                  })
              endpoint = `/api/questions/${ this.questionId }/topics/`;
              apiService(endpoint)
                  .then(data => {
                    if (data) {
                      this.questionTopics = data;
                      this.questionTopics.results.forEach((result) => {
                        if (result["count_votes"] >= 3) {
                          this.topicList.push(result);
                        }
                      });
                    }
                  })
              endpoint = `/api/labels/`;
              apiService(endpoint)
                  .then(data => {
                    if (data) {
                      this.allLabels = data;
                    }
                  })
              endpoint = `/api/topics/`;
              apiService(endpoint)
                  .then(data => {
                    if (data) {
                      this.allTopics = data;
                    }
                  })
        },
        onLabelSubmit() {
          let endpoint = `/api/questions/${ this.questionId }/labels/`;
          apiService(endpoint, "POST", {labelName: this.selectedLabelName, labelValue: this.selectedLabelValue})
          this.selectedLabelName = "";
          this.selectedLabelValue = "";
          this.getLabelsTopics();
          location.reload();
        },
        onTopicSubmit() {
            if (this.selectedTopicName) {
              this.selectedTopicName = this.selectedTopicName.toLowerCase();
              let endpoint = `/api/questions/${ this.questionId }/topics/`;
              apiService(endpoint, "POST", {topicName: this.selectedTopicName})
              this.selectedTopicName = "";
              this.getLabelsTopics();
              location.reload();
            }
        },
        isTopicExists(topicName) {
          if (!this.allTopics) {
            return false;
          }
          this.allTopics.results.forEach((result) => {
              if (result.topicName === topicName) {
                return true;
              }
          });
          return false;
        },
        onChange(result) {
          this.selectedTopicName = result;
        },
    },
    created() {
        this.getLabelsTopics();
    }
}
</script>

<style scoped>
body {
    opacity: 0;
}
.plus {
  width: 25px;
  height: auto;
}

.info {
  width: 29px;
  height: auto;
}
#close {
  width: 25px;
  height: auto;
}

#close2 {
  width: 25px;
  height: auto;
}

.topic-label-tag {
  font-size: 16px;
}

</style>