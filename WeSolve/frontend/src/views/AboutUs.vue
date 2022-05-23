<template>
  <div class="about-us">
    <div class="container mt-2">
      <div>
        <h2>
          What is <span class="aladin">WeSolve</span>?
        </h2>
        <p>
          <span class="aladin">WeSolve</span> is a platform for sharing and ranking solutions for university exams.
        </p>
        <p>
          Our goal is to create a learning community and help students to study better and pass the exams successfully.
        </p>
        <p>
          Students can register to <span class="aladin">WeSolve</span>, upload solutions to questions from past exams, and watch other students’ solutions to the same question.
        </p>
        <p>
          In addition, students can contribute to the <span class="aladin">WeSolve</span> community by labeling questions and ranking solutions, in order to improve the studying experience in the website and make it more accurate and efficient.
        </p>
        <h2>
          Why <span class="aladin">WeSolve</span>?
        </h2>
        <p>
          As university students during COVID-19, creating study groups for exams became more difficult since students were not physically in the campus, so making new connections with other students was hard.
        </p>
        <p>
          <span class="aladin">WeSolve</span> intends to fill this gap and make the studying experience a little bit more social and cooperative.
        </p>
        <hr>
      </div>
      <router-link
              :to="{ name: 'search' }" 
              class="btn btn-lg btn-info mb-3"
              type="button"
              >Get Started!
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "AboutUsView",
}
</script>

<style scoped>
  h2 {
    margin-bottom: 1em;
    margin-top: 1em;
  }

  p {
    font-size: 1.2em;
  }
</style>