<template>
  <div class="home">
    <div class="container mt-2">
      <div v-for="question in questions"
           :key="question.pk">
        <p class="mb-0">Posted by:
          <span class="question-author">{{ question.author }}</span>
        </p>
        <h2>
          <router-link
            :to="{ name: 'question', params: { slug: question.slug } }"
            class="question-link"
            >{{ question.content }}
          </router-link>
        </h2>
        <p>Answers: {{ question.answers_count }}</p>
        <hr>
      </div>
      <div class="my-4">
        <p v-show="loadingQuestions">...loading...</p>
        <button
          v-show="next"
          @click="getQuestions"
          class="btn btn-sm btn-outline-success"
          >Load More
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProfileView",
}
</script>

<style scoped>

</style>