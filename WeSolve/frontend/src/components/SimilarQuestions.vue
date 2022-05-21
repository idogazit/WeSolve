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
    </div>
</template>

<script>
export default {
    props: {
        questionSlug: {
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
            console.log(this.questionSlug)
            this.questions = [
                {
                    author: "ido gazit",
                    slug: "00000",
                    content: "best question",
                    answers_count: 20
                }
            ]
        },
        chooseQuestion(slug) {
            console.log(slug)
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