<template>
    <div class="jumbotron">
        <div class="container">
            <h1 class="mb-3">Similar Questions:</h1>
            <div v-for="(question, index) in questions"
                :key="question.pk">
                <p v-if="index == 0" class="mb-0">
                    {{ questionCrumb0.courseName }}
                    <span class="question-author">\</span>
                    {{ questionCrumb0.examTime}}
                </p>
                <p  v-if="index == 1" class="mb-0">
                    {{ questionCrumb1.courseName }}
                    <span class="question-author">\</span>
                    {{ questionCrumb1.examTime}}
                </p>
                <p v-if="index == 2" class="mb-0">
                    {{ questionCrumb2.courseName }}
                    <span class="question-author">\</span>
                    {{ questionCrumb2.examTime}}
                </p>
                <h2>
                    <button
                        @click="renderSimQuestion(question.slug, index, question.questionId)"
                        class="question-link"
                        >{{ question.content }}
                    </button>
                </h2>
                <p>Answers: {{ question.answers_count }}</p>
                <hr>
            </div>
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
    data () {
        return {
            questions: [],
            questionCrumb0: null,
            questionCrumb1: null,
            questionCrumb2: null
        }
    },
    methods: {
        getCourseName() {
            
            console.log(this.questionCrumbs[1].courseName)
            return this.questionCrumbs[1].courseName
        },
        getSimilarQuestion(newQuestionId) {
            // need to get the similar questions by the selected question slug
            let endpoint = `/api/questions/${ this.questionId }/similar/`;
            if (newQuestionId) {
                endpoint = `/api/questions/${ newQuestionId }/similar/`;
            }
              apiService(endpoint)
                  .then(data => {
                    if (data) {
                      this.questions = data.results;
                      for (let i = 0; i < data.results.length; i++) {
                        endpoint = `/api/nav/${ this.questions[i].examUniqueName }/crumbs/`;
                        apiService(endpoint)
                        .then(data2 => {
                            if (data2) {
                                    if (i == 0){
                                        this.questionCrumb0 = data2
                                    }
                                    if (i == 1){
                                        this.questionCrumb1 = data2
                                    }
                                    if (i == 2){
                                        this.questionCrumb2 = data2
                                    }
                                }
                            })
                        }
                    }
                  })
        },
        renderSimQuestion(slug, index, newQuestionId) {
            if (index == 0){
                this.$emit('renderSimQuestion', slug, this.questionCrumb0);
            }
            if (index == 1){
                this.$emit('renderSimQuestion', slug, this.questionCrumb1);
            }
            if (index == 2){
                this.$emit('renderSimQuestion', slug, this.questionCrumb2);
            }
            this.getSimilarQuestion(newQuestionId)
            window.scrollTo(0,0);
        }
    },
    created() {
        this.getSimilarQuestion()
    }
}
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