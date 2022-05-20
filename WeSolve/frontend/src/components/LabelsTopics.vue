<template>
    <div>
        <ul class="list-group list-group-horizontal-sm">
            <li class="list-group-item border-0 .flex-fill pr-1 pl-1 pd-3" v-for="topic in getTopics" :key="topic"><span class="badge badge-danger">{{ topic["topicName"] }}</span></li>
            <li class="list-group-item border-0 .flex-fill pr-1 pl-1 pd-3" v-for="label in getLabels" :key="label"><span class="badge badge-warning">{{ label["labelName"] }}: {{ label["labelValue"] }}</span></li>
            <li class="list-group-item border-0 .flex-fill pr-1 pl-1 pd-3"><img id="plus" src="https://img.icons8.com/external-tanah-basah-glyph-tanah-basah/48/26e07f/external-plus-essentials-tanah-basah-glyph-tanah-basah-2.png"/></li>
        </ul>
        <p class="label-form-title label">Add Label:</p>
        <form id="label-form" class="card label-submit" @submit.prevent="onSubmit">
            <select v-model="selectedLabelName">
                <option disabled selected id="defaultLabelName">Select Label</option>
                <option v-for="label in allLabels.results" :key="label">{{ label["labelName"] }}</option>
            </select>
            <select v-model="selectedLabelValue">
                <option disabled selected id="defaultLabelValue">Select Label Value</option>
                <option v-for="labelValue in getLabelValues" :key="labelValue">{{ labelValue }}</option>
            </select>
            <button
            type="submit"
            class="btn btn-success"
            >Submit Label
            </button>
        </form>
    </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
export default {
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
            selectedLabelName: "",
            selectedLabelValue: ""
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
        }
    },
    methods: {
        getLabelsTopics() {
            let endpoint = `/api/questions/${ this.questionId }/labels/`;
              apiService(endpoint)
                  .then(data => {
                    if (data) {
                      this.questionLabels = data;
                    }
                  })
              endpoint = `/api/questions/${ this.questionId }/topics/`;
              apiService(endpoint)
                  .then(data => {
                    if (data) {
                      this.questionTopics = data;
                    }
                  })
              endpoint = `/api/labels/`;
              apiService(endpoint)
                  .then(data => {
                    if (data) {
                      this.allLabels = data;
                    }
                  })
        },
        onSubmit() {
      // Tell the REST API to create a new answer for this question based on the user input, then update some data properties
            let endpoint = `/api/questions/${this.questionId}/labels/`;
            apiService(endpoint, "POST", {labelName: this.selectedLabelName, labelValue: this.selectedLabelValue})
            this.labelSubmit = false;
            this.selectedLabelName = "";
            this.selectedLabelValue = "";
    
            this.questionLabels = [];
            this.questionTopics = [];
            this.getLabelsTopics();
        }
    },
    created() {
        this.getLabelsTopics();
    }
}
</script>

<style scoped>
.label-submit {
  width: 20%;
  margin: 0;
  margin-left: auto;
  margin-right: auto;
  padding: 20px;
}

.label-form-title {
  margin: 0;
  margin-left: auto;
  margin-right: auto;
  position: relative;
  left: 50%;
  display: inline-block;
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
}
#plus {
  width: 25px;
  height: auto;
}
</style>