<template>
  <div class="home">
    <Breadcrumb :crumbs="crumbs" @selected="selected" />
    <SelectNext v-if="showNav" :links="links" :level="level[crumbs.length]" @selectedLink="selectedLink" />
    <div v-if="showQuestions" class="container mt-2">
      <div v-for="question in questions"
           :key="question.pk">
        <p class="mb-0">Posted by:
          <span class="question-author">{{ question.author }}</span>
        </p>
        <h2>
          <button
            @click="chooseQuestion(question.slug)"
            class="question-link"
            >{{ question.content }}
          </button>
        </h2>
        <p>Answers: {{ question.answers_count }}</p>
        <hr>
      </div>
    </div>
    <QuestionView v-if="showChosenQuestion" :slug="chosenQuestionSlug" />
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import Breadcrumb from "@/components/BreadCrumb.vue";
import SelectNext from "@/components/SelectNext.vue";
import QuestionView from "@/components/Question.vue";
export default {
  name: "HomeView",
  components: {
    Breadcrumb,
    SelectNext,
    QuestionView
  },
  data() {
    return {
      questions: [],
      crumbs: ['TAU'],
      level: ['university', 'faculty', 'school', 'course', 'exam', 'question'],
      links: [],
      examsId: [],
      showQuestions: false,
      showNav: true,
      showChosenQuestion: false,
      chosenQuestionSlug: null
    }
  },
  methods: {
    chooseQuestion(slug) {
      this.showChosenQuestion = true
      this.showQuestions = false
      this.showNav = false
      this.chosenQuestionSlug = slug
    },
    getQuestions(examId) {
      this.showQuestions = true
      // make a GET Request to the questions list endpoint and populate the questions array
      let endpoint = "/api/nav/" + examId + "/questions/";
      apiService(endpoint)
        .then(data => {
          this.questions.push(...data.results)
        })
    },
    loadUpTAU(){
      let endpoint = "/api/nav/faculties/"
      apiService(endpoint)
          .then(data => {
            this.links = data["results"]
        })
    },
    selected(crumb, ci) {
      this.showNav = true
      this.showQuestions = false
      this.showChosenQuestion = false
      this.crumbs = this.crumbs.slice(0, ci + 1)

      const reqLevel = this.level[this.crumbs.length]
      console.log(reqLevel)

      let endpoint
      if (this.crumbs.length == 1) {
        endpoint = "/api/nav/faculties/"
      } else {
        endpoint = "/api/nav/" + crumb + "/" + this.level[this.crumbs.length] + "s/"
      }
      if (reqLevel == 'exam') {
          apiService(endpoint)
          .then(data => {
            this.links = data["results"].map(({ examTime }) => examTime)
            this.examsId = data["results"].map(({ examId }) => examId)
          })
        } else {
          apiService(endpoint)
          .then(data => {
            this.links = data["results"]
          })
        }
    },
    selectedLink(link, linkIndex) {
      const reqLevel = this.level[this.crumbs.length + 1]
      if (reqLevel == 'question'){
        this.showNav = false
        this.getQuestions(this.examsId[linkIndex])
      } else {
        let endpoint = "/api/nav/" + link + "/" + reqLevel + "s/"
        if (reqLevel == 'exam') {
          apiService(endpoint)
          .then(data => {
            this.links = data["results"].map(({ examTime }) => examTime)
            this.examsId = data["results"].map(({ examId }) => examId)
          })
        } else {
          apiService(endpoint)
          .then(data => {
            this.links = data["results"]
          })
        }
      }
      this.crumbs.push(link)
    }
  },
  created() {
    //this.getQuestions()
    document.title = "WeSolve";
    this.loadUpTAU()
  }
};
</script>

<style scoped>
.question-author {
  font-weight: bold;
  color: #DC3545;
}

.question-link {
  font-weight: bold;
  color: black;
  padding: 0;
  border: none;
  background: none;
}

.question-link:hover {
  color: #343A40;
  text-decoration: none;
}
</style>
