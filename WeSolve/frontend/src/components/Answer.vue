<template>
  <div class="single-answer">
    <p class="text-muted">
      <strong>{{ answer.author }}</strong> &#8901; {{ answer.created_at }}
    </p>
    <div v-if="!is_spammer">
      <button
        class="btn btn-sm mr-1"
        @click="toggleUpvote"
        :class="{
          'btn-success': userUpvotedAnswer,
          'btn-outline-success': !userUpvotedAnswer,
          }"
        :disabled="userDownvotedAnswer || isAnswerAuthor"
        ><strong>Upvote [{{ upvotesCounter }}]</strong>
      </button>
      <button
        class="btn btn-sm  mr-1"
        @click="toggleDownvote"
        :class="{
          'btn-danger': userDownvotedAnswer,
          'btn-outline-danger': !userDownvotedAnswer
          }"
        :disabled="userUpvotedAnswer || isAnswerAuthor"
        ><strong>Downvote [{{ downvotesCounter }}]</strong>
      </button>
       <!-- "https://img.icons8.com/dotty/80/26e07f/assessments.png" -->
      <img class="mr-1" id="teacherApproval" v-if="answer.is_teacher_approved" src="https://img.icons8.com/officel/40/000000/test-partial-passed.png" />
      <label id="teacherLine" class="aladin" v-if="answer.is_teacher_approved">This answer is approved by a teacher!</label>
    </div>
    <p>{{ answer.body }}</p>
    <div v-if="answer.answerPDF !==null">
      <embed :src="getAnswerPDF" type="application/pdf" frameBorder="0" scrolling="auto" height="700px" width="100%">
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
      userUpvotedAnswer: this.answer.user_has_upvoted,
      upvotesCounter: this.answer.upvotes_count,
      userDownvotedAnswer: this.answer.user_has_downvoted,
      downvotesCounter: this.answer.downvotes_count,
      is_spammer: false
    }
  },
  computed: {
    isAnswerAuthor() {
      // return true if the logged in user is also the author of the answer instance
      return this.answer.author === this.requestUser;
    },
    getAnswerPDF() {
      var pdf_name = this.answer["answerPDF"].split('/')[(this.answer["answerPDF"].split('/')).length - 1]
      return "../../../questions/uploads/answersPDF/".concat(pdf_name).concat("/");
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
      let endpoint = `/api/answers/${ this.answer.answerId }/upvote/`;
      apiService(endpoint, "POST")
    },
    unUpvoteAnswer() {
      this.userUpvotedAnswer = false;
      this.upvotesCounter -= 1;
      let endpoint = `/api/answers/${ this.answer.answerId }/upvote/`;
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
      let endpoint = `/api/answers/${ this.answer.answerId }/downvote/`;
      apiService(endpoint, "POST")
    },
    unDownvoteAnswer() {
      this.userDownvotedAnswer = false;
      this.downvotesCounter -= 1;
      let endpoint = `/api/answers/${ this.answer.answerId }/downvote/`;
      apiService(endpoint, "DELETE")
    },
    triggerDeleteAnswer() {
      // emit an event to delete an answer instance
      this.$emit("delete-answer", this.answer)
    },
    setSpammer() {
      // the username has been set to localStorage by the App.vue component
      let endpoint = "/api/users/current/";
      apiService(endpoint)
        .then(data => {
          if (data["rankScore"] < -100){
            this.is_spammer = true;
          }   
        })
    }
  },
  created() {
    this.setSpammer();
  },
}
</script>
<style>
#teacherApproval {
  width: 35px;
  height: auto;
}
#teacherLine {
  color: #25e180;
  color: #daac63;
  font-size: 20px;
}
</style>