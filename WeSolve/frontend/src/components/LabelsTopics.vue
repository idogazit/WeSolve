<template>
    <div>
        <ul class="list-group list-group-horizontal-sm">
            <li class="list-group-item border-0 .flex-fill pr-1 pl-1 pd-3" v-for="topic in getTopics" :key="topic"><span class="badge badge-danger">{{ topic["topicName"] }}</span></li>
            <li class="list-group-item border-0 .flex-fill pr-1 pl-1 pd-3" v-for="label in getLabels" :key="label"><span class="badge badge-warning">{{ label["labelName"] }}: {{ label["labelValue"] }}</span></li>
            <li v-if="showForm == false" class="list-group-item border-0 .flex-fill pr-1 pl-1 pd-3">
                <button class="btn btn-default m-0 p-0" data-bs-toggle="tooltip" data-bs-placement="top" title="Add Label">
                    <img @click="enableShowForm" id="plus" src="https://img.icons8.com/external-tanah-basah-glyph-tanah-basah/48/26e07f/external-plus-essentials-tanah-basah-glyph-tanah-basah-2.png" />
                </button>
            </li>
            <li  class="list-group-item border-0 .flex-fill pr-1 pl-1 pd-3">
            </li>
        </ul>
        <div v-if="showForm" class="container">
            
            <form id="label-form" class="form-inline" @submit.prevent="onSubmit">
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
            selectedLabelValue: "",
            showForm: false
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
            let endpoint = `/api/questions/${ this.questionId }/labels/`;
            apiService(endpoint, "POST", {labelName: this.selectedLabelName, labelValue: this.selectedLabelValue})
            this.labelSubmit = false;
            this.selectedLabelName = "";
            this.selectedLabelValue = "";
            this.getLabelsTopics();
        }
    },
    created() {
        this.getLabelsTopics();
    }
}
</script>

<style scoped>
#plus {
  width: 25px;
  height: auto;
}
#close {
  width: 25px;
  height: auto;
}
</style>