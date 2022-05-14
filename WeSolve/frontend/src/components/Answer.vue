<template>
  <div class="single-answer">
    <p class="text-muted">
      <strong>{{ answer.author }}</strong> &#8901; {{ answer.created_at }}
    </p>
    <p>{{ answer.body }}</p>
    <p>
      <embed :src="getAnswerPDF" type="application/pdf" frameBorder="0" scrolling="auto" height="1000px" width="80%">
    </p>
    <div>
      <button
        class="btn btn-sm"
        @click="toggleUpvote"
        :class="{
          'btn-success': userUpvotedAnswer,
          'btn-outline-success': !userUpvotedAnswer,
          }"
        :disabled=userDownvotedAnswer
        ><strong>Upvote [{{ upvotesCounter }}]</strong>
      </button>
      <button
        class="btn btn-sm"
        @click="toggleDownvote"
        :class="{
          'btn-danger': userDownvotedAnswer,
          'btn-outline-danger': !userDownvotedAnswer
          }"
        :disabled=userUpvotedAnswer
        ><strong>Downvote [{{ downvotesCounter }}]</strong>
      </button>
    </div>
    <hr>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "AnswerComponent",
  props: {
    answer: {
      type: Object,
      required: true
    },
    requestUser: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      userUpvotedAnswer: this.answer.user_has_voted, // TODO: needs to be replaced with user_has_upvoted
      upvotesCounter: this.answer.likes_count, // TODO: needs to be replaced with upvotes_count
      userDownvotedAnswer: this.answer.user_has_downvoted,
      downvotesCounter: this.answer.downvotes_count,
    }
  },
  computed: {
    isAnswerAuthor() {
      // return true if the logged in user is also the author of the answer instance
      return this.answer.author === this.requestUser;
    },
    getAnswerPDF() {
      const url = this.answer["answerPDF"].replace("http://localhost:8000/api/questions/".concat(this.answer["question_slug"]).concat("/answers/questions/uploads/answersPDF/"), "");
      return "../../../questions/uploads/answersPDF/".concat(url).concat("/");
    },
  },
  methods: {
    toggleUpvote() {
      this.userUpvotedAnswer === false
        ? this.upvoteAnswer()
        : this.unUpvoteAnswer()
    },
    upvoteAnswer() {
      this.userUpvotedAnswer = true;
      this.upvotesCounter += 1;
      let endpoint = `/api/answers/${ this.answer.id }/like/`;
      apiService(endpoint, "POST")
    },
    unUpvoteAnswer() {
      this.userUpvotedAnswer = false;
      this.upvotesCounter -= 1;
      let endpoint = `/api/answers/${ this.answer.id }/like/`;
      apiService(endpoint, "DELETE")
    },
    toggleDownvote() {
      this.userDownvotedAnswer === false
        ? this.downvoteAnswer()
        : this.unDownvoteAnswer()
    },
    downvoteAnswer() {
      this.userDownvotedAnswer = true;
      this.downvotesCounter += 1;
      let endpoint = `/api/answers/${ this.answer.id }/like/`;
      apiService(endpoint, "POST")
    },
    unDownvoteAnswer() {
      this.userDownvotedAnswer = false;
      this.downvotesCounter -= 1;
      let endpoint = `/api/answers/${ this.answer.id }/like/`;
      apiService(endpoint, "DELETE")
    },
    triggerDeleteAnswer() {
      // emit an event to delete an answer instance
      this.$emit("delete-answer", this.answer)
    },
  }
}
</script>

