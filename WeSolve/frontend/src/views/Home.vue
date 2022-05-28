<template>
  <div class="home">
    <Breadcrumb :crumbs="crumbs" :inQuestion="showChosenQuestion" @selected="selected" />
    <SelectNext v-if="showNav" :links="links" :level="level[crumbs.length]" @selectedLink="selectedLink" />
    <div v-if="showQuestions" class="container mt-2">
      <div v-for="question in questions"
           :key="question.pk">
        <h2>
          <button
            @click="chooseQuestion(question.slug)"
            class="question-link"
            >{{ question.content }}
          </button>
        </h2>
        <p>
          <img class="answer-icon" src="https://img.icons8.com/windows/32/000000/chat-message.png"/>
          Answers: <span class="question-author"> {{ question.answers_count }}</span></p>
        <hr>
      </div>
    </div>
    <QuestionView v-if="showChosenQuestion" :slug="chosenQuestionSlug" @renderCrumbsAndExamId="renderCrumbsAndExamId" />
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
      chosenQuestionSlug: null,
      chosenExamIndex: null
    }
  },
  mounted() {
    if (localStorage.questions) {
      this.questions = JSON.parse(localStorage.questions);
    }
    if (localStorage.crumbs) {
      this.crumbs = JSON.parse(localStorage.crumbs);
    }
    if (localStorage.links) {
      this.links = JSON.parse(localStorage.links);
    }
    if (localStorage.examsId) {
      this.examsId = JSON.parse(localStorage.examsId);
    }
    
    if (localStorage.showQuestions) {
      this.showQuestions = JSON.parse(localStorage.showQuestions);
    }
    if (localStorage.showNav) {
      this.showNav = JSON.parse(localStorage.showNav);
    }
    if (localStorage.showChosenQuestion) {
      this.showChosenQuestion = JSON.parse(localStorage.showChosenQuestion);
    }
    if (localStorage.chosenQuestionSlug) {
      this.chosenQuestionSlug = JSON.parse(localStorage.chosenQuestionSlug);
    }
    if (localStorage.chosenExamIndex) {
      this.chosenExamIndex = JSON.parse(localStorage.chosenExamIndex);
    }

    if (this.crumbs.length === 1) {
      this.loadUpTAU()
    }
  },
  watch: {
    questions: {
      handler(newQuestions){
        localStorage.questions = JSON.stringify(newQuestions);
      },
      deep: true
    },
    crumbs: {
      handler(newCrumbs){
        localStorage.crumbs = JSON.stringify(newCrumbs);
      },
      deep: true
    },
    links: {
      handler(newLinks){
        localStorage.links = JSON.stringify(newLinks);
      },
      deep: true
    },
    examsId: {
      handler(newExamsId){
        localStorage.examsId = JSON.stringify(newExamsId);
      },
      deep: true
    },

    showQuestions: {
      handler(newShowQuestions){
        localStorage.showQuestions = JSON.stringify(newShowQuestions);
      }
    },
    showNav: {
      handler(newShowNav){
        localStorage.showNav = JSON.stringify(newShowNav);
      }
    },
    showChosenQuestion: {
      handler(newShowChosenQuestion){
        localStorage.showChosenQuestion = JSON.stringify(newShowChosenQuestion);
      }
    },
    chosenQuestionSlug: {
      handler(newChosenQuestionSlug){
        localStorage.chosenQuestionSlug = JSON.stringify(newChosenQuestionSlug);
      }
    },
    chosenExamIndex: {
      handler(newChosenExamIndex){
        localStorage.chosenExamIndex = JSON.stringify(newChosenExamIndex);
      }
    },
  },
  methods: {
    renderCrumbsAndExamId(questionCrumbs) {
      let newCrumbs = ['TAU']
      newCrumbs.push(questionCrumbs.facultyName)
      newCrumbs.push(questionCrumbs.schoolName)
      newCrumbs.push(questionCrumbs.courseName)
      newCrumbs.push(questionCrumbs.examTime)
      this.crumbs = newCrumbs
      this.examsId = [questionCrumbs.examId]
      this.chosenExamIndex = 0
      this.$forceUpdate();
    },
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
      this.chosenQuestionSlug = null
      this.questions = []
      this.crumbs = this.crumbs.slice(0, ci + 1)

      const reqLevel = this.level[this.crumbs.length]
      console.log(reqLevel)
      if (reqLevel == 'question'){
        this.showNav = false
        this.getQuestions(this.examsId[this.chosenExamIndex])
      } else {
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
      }
    },
    selectedLink(link, linkIndex) {
      const reqLevel = this.level[this.crumbs.length + 1]
      if (reqLevel == 'question'){
        this.showNav = false
        this.chosenExamIndex = linkIndex
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
  },
  beforeDestroy() {
    localStorage.clear()
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

.answer-icon {
  width: 25px;
  height: auto;
}
</style>
