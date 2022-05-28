<template>
  <div class="single-question mt-2">
    <div v-if="question" class="container">
      <h1>{{ question.content }}</h1>
      <QuestionActions
        v-if="isQuestionAuthor"
        :slug="question.slug"
      />
      <p>{{ question.created_at }}</p>
      <p v-if="!is_spammer">
      <LabelsTopics :questionId="question.questionId" />
      </p>
      <p>
        <embed :src="getQuestionPDF" type="application/pdf" frameBorder="0" scrolling="auto" height="600px" width="100%">
      </p>
      <hr>
      <div v-if="userHasAnswered">
        <p class="answer-added">You've written an answer!</p>
      </div>
      <div v-else-if="is_spammer">
        <p class="answer-added" style="color:red">Your rank score is too low to perform any action! Contact the admin!</p>
      </div>
      <div v-else-if="showForm">
        <form class="card" enctype="multipart/form-data" @submit.prevent="onSubmit">
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
    </div>
    <SimilarQuestions :questionId="question.questionId" @renderSimQuestion="renderSimQuestion"/>
  </div>
</template>

<script>
import axios from 'axios';
import { apiService } from "@/common/api.service.js";
import { CSRF_TOKEN } from "@/common/csrf_token.js"
import AnswerComponent from "@/components/Answer.vue";
import QuestionActions from "@/components/QuestionActions.vue";
import LabelsTopics from "@/components/LabelsTopics.vue";
import SimilarQuestions from "@/components/SimilarQuestions.vue";
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
    QuestionActions,
    LabelsTopics,
    SimilarQuestions
  },
  data() {
    return {
      question: {},
      answers: [],
      next: null,
      newAnswerBody: null,
      error: null,
      userHasAnswered: false,
      showForm: false,
      requestUser: null,
      answerPDF: null,
      is_spammer: false,
      form: {
                body: "",
                answerPDF: null,
      },
      newSlug: null
    }
  },
  beforeMounted() {
    if (localStorage.newSlug) {
      this.newSlug = localStorage.newSlug;
    }
  },
  watch: {
    newSlug: {
      handler(newerSlug){
        localStorage.newSlug = newerSlug;
        }
    },
  },
  computed: {
    isQuestionAuthor() {
      // return true if the logged in user is also the author of the question instance
      return this.question.author === this.requestUser;
    },
    getQuestionPDF() {
      var pdf_name = this.question["questionPDF"].split('/')[(this.question["questionPDF"].split('/')).length - 1];
      return "../../../questions/uploads/questionsPDF/".concat(pdf_name).concat("/");
    }
  },
  methods: {
    renderSimQuestion(slug, questionCrumbs) {
      this.newSlug = slug
      this.getQuestionData()
      this.getQuestionAnswers()
      this.$emit('renderCrumbsAndExamId', questionCrumbs);
      location.reload();
    },
    setPageTitle(title) {
      // set a given title string as the webpage title
      document.title = title;
    },
    setRequestUser() {
      // the username has been set to localStorage by the App.vue component
      this.requestUser = window.localStorage.getItem("username");
      let endpoint = "/api/users/current/";
      apiService(endpoint)
        .then(data => {
          if (data["rankScore"] < -100){
            this.is_spammer = true;
          }   
        })
    },
    getQuestionData() {
      // get the details of a question instance from the REST API and call setPageTitle
      let endpoint = `/api/questions/${this.slug}/`;
      if (this.newSlug) {
        endpoint = `/api/questions/${this.newSlug}/`;
      }
      apiService(endpoint)
          .then(data => {
            if (data) {
              this.question = data;
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
      if (this.newSlug) {
        endpoint = `/api/questions/${this.newSlug}/answers/`;
      }
      console.log(endpoint)
      if (this.next) {
        endpoint = this.next;
      }
      apiService(endpoint)
          .then(data => {
            this.answers.push(...data.results);
            if (data.next) {
              this.next = data.next;
            } else {
              this.next = null;
            }
          })
    },
    uploadFile(e) {
      this.answerPDF = e.target.files[0];
    },
    onSubmit() {
      // Tell the REST API to create a new answer for this question based on the user input, then update some data properties
      let formData = new FormData();
      if (!this.newAnswerBody && !this.answerPDF) {
        this.error = "You can't send an empty answer!";
      } else {
        if (this.newAnswerBody) {
          formData.append("body", this.newAnswerBody);
        }
        if (this.answerPDF) {
          formData.append("answerPDF",this.answerPDF);
        }

        let config = {
          headers: {
            'X-CSRFTOKEN': CSRF_TOKEN
          }
        }

        axios
          .post(`/api/questions/${this.slug}/answer/`, formData, config)
          .then(data => {
              location.reload();
              this.answers.unshift(data)
            })

        this.newAnswerBody = null;
        this.answerPDF = null;
        this.form = {
                body: "",
                answerPDF: null,
        };
        this.showForm = false;
        this.userHasAnswered = true;
        if (this.error) {
          this.error = null;
        }
      }
      this.getQuestionData();
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
    if (localStorage.newSlug) {
      this.newSlug = localStorage.newSlug;
    }
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

.submit-ans {
  margin-top: 10px;
  display: block;
}
</style>
