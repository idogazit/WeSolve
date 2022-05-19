<template>
  <div class="home">
    <div class="container mt-2">
      <div class="my-4">
        <h2>User Profile</h2>
        <img :src="userPic" alt="">
        <h3>{{ this.userFullName }}</h3>
        <div>
          <p class="user-details">{{ this.userEmail }}</p>
        </div>
        <div v-if="userIsTeacher">
          <p class="user-details">&#127891; Teacher &#127891;</p>
        </div>
        <div v-else>
          <p class="user-details">&#127894; Rank: {{ this.userRank }} &#127894;</p>
        </div>
        <!--<ul>
          <li><h4 class="my-courses">My Courses:</h4></li>
          <li v-for="course in userCourses" :key="course">
            &#127891; {{ course.replace("_", " - ") }}
          </li>
        </ul>-->
      </div>
    </div>
  </div>
</template>

<script>
import {apiService} from "@/common/api.service";

export default {
  name: "ProfileView",
  data () {
    return {
      userFullName: "",
      userEmail: "",
      userRank: "",
      userPic: "",
      userIsTeacher: false,
      userCourses: null,
      rankMap: {
        0 : "Freshman",
        1 : "Junior",
        2 : "Senior",
      },
    }
  },
  methods: {
    getUserInfo() {
      let endpoint = "/api/users/current/";
      apiService(endpoint)
        .then(data => {
          this.userFullName = data["first_name"].concat(" ", data["last_name"]);
          this.userEmail = data["email"];
          this.userRank= this.rankMap[data["rank"]];
          var pic_name = data["userPic"].split('/')[data["userPic"].split('/').length - 1]
          this.userPic = require("../../../users/uploads/userPics/".concat(pic_name));
          this.userIsTeacher = data["isTeacher"];
          this.userCourses = data["courses"];
        })
    }
  },
  created() {
    this.getUserInfo()
  }
};
</script>

<style scoped>

h2 {
  margin: 0;
  margin-top: 1em;
  margin-left: auto;
  margin-right: auto;
  position: relative;
  display: inline-block;
  top: 10%;
  left: 50%;
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
}

h3 {
  margin: 0;
  margin-bottom: 0.1em;
  margin-top: 1em;
  margin-left: auto;
  margin-right: auto;
  padding: 12px;
  position: relative;
  display: inline-block;
  left: 50%;
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  background-color: #98c9ef;
  border-radius: 30px 30px 30px 30px;
}

img {
  object-fit: cover;
  border: 1px solid #ddd;
  border-radius: 50%;
  padding: 5px;
  display: block;
  margin-bottom: 1em;
  margin-top: 1em;
  margin-left: auto;
  margin-right: auto;
  vertical-align: middle;
  width: 250px;
  height: 250px;
  position: relative;
}

.user-details {
  margin: 0.5em;
  margin-left: auto;
  margin-right: auto;
  position: relative;
  display: inline-block;
  left: 50%;
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  font-size: 1.3em;
}

.my-courses {
  margin: 1em;
  margin-left: auto;
  margin-right: auto;
  position: relative;
  display: inline-block;
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  font-size: 1.3em;
}

li {
  list-style-type: none;
}

</style>