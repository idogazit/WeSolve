<template>
  <div class="single-question mt-2">
    <div v-if="question" class="container">
      <h1>{{ question.content }}</h1>
      <QuestionActions
        v-if="isQuestionAuthor"
        :slug="question.slug"
      />
      <p class="mb-0">Posted by:
        <span class="author-name">{{ question.author }}</span>
      </p>
      <p>{{ question.created_at }}</p>
      <ul>
        <li class="topic label" v-for="topic in getTopics" :key="topic">{{ topic["topicName"] }}</li>
      </ul>
      <ul>
        <li class="qlabel label" v-for="label in getLabels" :key="label">{{ label["labelName"] }}: {{ label["labelValue"] }}</li>
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
          @click="labelSubmit = true"
          >Submit Label
        </button>
      </form>
      <p>
        <embed :src="getQuestionPDF" type="application/pdf" frameBorder="0" scrolling="auto" height="600px" width="100%">
      </p>
      <hr>
      <div v-if="userHasAnswered">
        <p class="answer-added">You've written an answer!</p>
      </div>
      <div v-else-if="showForm">
        <form class="card" @submit.prevent="onSubmit">
          <div class="card-header px-3">
            Answer the Question
          </div>
          <div class="card-block">
            <textarea 
              v-model="newAnswerBody"
              class="form-control"
              placeholder="Share Your Knowledge!"
              rows="5"
            ></textarea>
          </div>
          <div class="card-footer px-3">
            <input class="upload-pdf" type="file" name="upload" accept="application/pdf" @change="uploadFile"/>
            <button type="submit" class="btn btn-sm btn-success submit-ans">Submit Your Answer</button>
          </div>
        </form>
        <p v-if="error" class="error mt-2">{{ error }}</p>
      </div>
      <div v-else>
        <button
          class="btn btn-sm btn-success"
          @click="showForm = true"
          >Answer the Question
        </button>
      </div>
      <hr>
    </div>
    <div v-else>
      <h1 class="error text-center">404 - Question Not Found</h1>
    </div>
    <div v-if="question" class="container">
      <AnswerComponent 
        v-for="answer in answers"
        :answer="answer"
        :requestUser="requestUser"
        :key="answer.id"
        @delete-answer="deleteAnswer"
      />
      <div class="my-4">
        <p v-show="loadingAnswers">...loading...</p>
        <button
          v-show="next"
          @click="getQuestionAnswers"
          class="btn btn-sm btn-outline-success"
          >Load More
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import AnswerComponent from "@/components/Answer.vue";
import QuestionActions from "@/components/QuestionActions.vue";
export default {
  name: "QuestionView",
  props: {
    slug: {
      type: String,
      required: true
    },
  },
  components: {
    AnswerComponent,
    QuestionActions
  },
  data() {
    return {
      question: {},
      answers: [],
      next: null,
      loadingAnswers: false,
      newAnswerBody: null,
      error: null,
      userHasAnswered: false,
      showForm: false,
      requestUser: null,
      questionLabels: [],
      questionTopics: [],
      allLabels: [],
      selectedLabelName: "",
      selectedLabelValue: "",
      labelSubmit: false,
      answerUploadPDF: null,
    }
  },
  computed: {
    isQuestionAuthor() {
      // return true if the logged in user is also the author of the question instance
      return this.question.author === this.requestUser;
    },
    getQuestionPDF() {
      var pdf_name = this.question["questionPDF"].split('/')[(this.question["questionPDF"].split('/')).length - 1];
      return "../../../questions/uploads/questionsPDF/".concat(pdf_name).concat("/");
    },
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
  },
  methods: {
    setPageTitle(title) {
      // set a given title string as the webpage title
      document.title = title;
    },
    setRequestUser() {
      // the username has been set to localStorage by the App.vue component
      this.requestUser = window.localStorage.getItem("username");
    },
    getQuestionData() {
      // get the details of a question instance from the REST API and call setPageTitle
      let endpoint = `/api/questions/${this.slug}/`;
      apiService(endpoint)
          .then(data => {
            if (data) {
              this.question = data;
              endpoint = `/api/questions/${this.question["questionId"]}/labels/`;
              apiService(endpoint)
                  .then(data => {
                    if (data) {
                      this.questionLabels = data;
                    }
                  })
              endpoint = `/api/questions/${this.question["questionId"]}/topics/`;
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
              this.userHasAnswered = data.user_has_answered;
              this.setPageTitle(data.content)
            } else {
              this.question = null;
              this.setPageTitle("404 - Page Not Found")
            }
          })
    },
    getQuestionAnswers() {
      // get a page of answers for a single question from the REST API's paginated 'Questions Endpoint'
      let endpoint = `/api/questions/${this.slug}/answers/`;
      if (this.next) {
        endpoint = this.next;
      }
      this.loadingAnswers = true;
      apiService(endpoint)
          .then(data => {
            this.answers.push(...data.results);
            this.loadingAnswers = false;
            if (data.next) {
              this.next = data.next;
            } else {
              this.next = null;
            }
          })
    },
    getQuestionLabels() {
      let endpoint = `/api/questions/${this.question["questionId"]}/labels/`;
      apiService(endpoint)
          .then(data => {
            if (data) {
              this.questionLabels = data;
            }
          })
    },
    onSubmit() {
      // Tell the REST API to create a new answer for this question based on the user input, then update some data properties
      if (this.labelSubmit) {
        let endpoint = `/api/questions/${this.question["questionId"]}/labels/`;
        apiService(endpoint, "POST", {labelName: this.selectedLabelName, labelValue: this.selectedLabelValue})
        this.labelSubmit = false;
        this.selectedLabelName = "";
        this.selectedLabelValue = "";
      } else {
        let answerData = {};
        if (!this.newAnswerBody && !this.answerUploadPDF) {
          this.error = "You can't send an empty answer!";
        } else {
          if (this.newAnswerBody) {
            answerData.body = this.newAnswerBody;
          }
          if (this.answerUploadPDF) {
            answerData.answerPDF = this.answerUploadPDF;
          }
          let endpoint = `/api/questions/${this.slug}/answer/`;
          apiService(endpoint, "POST", answerData)
              .then(data => {
                this.answers.unshift(data)
              })
          this.newAnswerBody = null;
          this.showForm = false;
          this.userHasAnswered = true;
          if (this.error) {
            this.error = null;
          }
        }
      }
      this.questionLabels = [];
      this.questionTopics = [];
      this.getQuestionData();
    },
    uploadFile() {
      this.answerUploadPDF = this.$refs.file.files[0];
    },
    async deleteAnswer(answer) {
      // delete a given answer from the answers array and make a delete request to the REST API
      let endpoint = `/api/answers/${answer.id}/`;
      try {
        await apiService(endpoint, "DELETE")
        this.$delete(this.answers, this.answers.indexOf(answer))
        this.userHasAnswered = false;
      }
      catch (err) {
        console.log(err)
      }
    }
  },
  created() {
    this.getQuestionData()
    this.getQuestionAnswers()
    this.setRequestUser()
  },
}
</script>

<style scoped>
.author-name {
  font-weight: bold;
  color: #DC3545;
}

.answer-added {
  font-weight: bold;
  color: green;
}

.error {
  font-weight: bold;
  color: red; 
}

.topic {
  margin: 0;
  margin-top: 1.2em;
  margin-left: auto;
  margin-right: auto;
  padding: 10px;
  position: relative;
  display: inline-block;
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  background-color: #98c9ef;
  border-radius: 30px 30px 30px 30px;
}

.qlabel {
  margin: 0;
  margin-left: auto;
  margin-right: auto;
  padding: 10px;
  position: relative;
  display: inline-block;
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  background-color: #ec8fb5;
  border-radius: 30px 30px 30px 30px;
}

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

.submit-ans {
  margin-top: 10px;
  display: block;
}

</style>
