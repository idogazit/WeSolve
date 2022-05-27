<template>
    <div class="jumbotron">
        <div class="container">
            <h1 class="mb-3">Similar Questions:</h1>
            <div v-for="question in questions"
                :key="question.pk">
                <p class="mb-0">Posted by:
                    <span class="question-author">{{ question.author }}</span>
                </p>
                <h2>
                <router-link :to="{ name: 'question',  params: {slug: question.slug} }" >
                    <button
                        class="question-link"
                        >{{ question.content }}
                    </button>
                </router-link>
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
            questions: []
        }
    },
    methods: {
        getSimilarQuestion() {
            // need to get the similar questions by the selected question slug
            let endpoint = `/api/questions/${ this.questionId }/similar/`;
              apiService(endpoint)
                  .then(data => {
                    if (data) {
                      this.questions = data.results;
                    }
                  })
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