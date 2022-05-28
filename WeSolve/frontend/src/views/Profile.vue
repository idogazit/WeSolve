<template>
  <div class="home">
    <div class="container mt-2">
      <div class="my-4">
        <h2>User Profile</h2>
        <img :src="userPic" alt="">
        <h3 class="badge badge-info">{{ this.userFullName }}</h3>
        <div>
          <p class="user-details">{{ this.userEmail }}</p>
        </div>
        <div v-if="userIsTeacher">
          <p class="user-details">&#127891; Teacher &#127891;</p>
        </div>
        <div v-else>
          <p class="user-details">&#127894; Rank: {{ this.userRank }} &#127894;</p>
        </div>
        <div class="container">
          <div v-if="userRankScore >= 0" class="row">
            <div class="col-md-6 mx-auto">
                <div class="progress" style="height: 50px;">
                  <div 
                    class="progress-bar bg-info progress-bar-striped progress-bar-animated" 
                    role="progressbar" 
                    :style="getStyleForProgessBar()"
                    :aria-valuenow="getNormalizedRank()" 
                    aria-valuemin="0" 
                    aria-valuemax="100"
                    >
                  </div>  
                </div>
                 <span class="aladin" style="font-size: 16px;">
                  {{this.userRankScore}}/{{this.progressBarMax}}
                </span>
            </div>
          </div>
          <div v-if="userRankScore < 0 && userRankScore > -101" class="row">
            <div class="col-md-6 mx-auto">
                <div class="progress" style="height: 50px;">
                  <div 
                    class="progress-bar bg-warning progress-bar-striped progress-bar-animated" 
                    role="progressbar" 
                    style="width: 100%; font-size: 25px;"
                    aria-valuenow="100" 
                    aria-valuemin="0" 
                    aria-valuemax="100"
                    >
                    {{this.userRankScore}}
                  </div>  
                </div>
                <span class="aladin" style="font-size: 20px;">
                  You have a negative rank of {{this.userRankScore}} ! Please try harder to support the community !
                </span>
            </div>
          </div>
          <div v-if="userRankScore < -100" class="row">
            <div class="col-md-6 mx-auto">
                <div class="progress" style="height: 50px;">
                  <div 
                    class="progress-bar bg-danger progress-bar-striped progress-bar-animated" 
                    role="progressbar" 
                    style="width: 100%; font-size: 25px;"
                    aria-valuenow="100" 
                    aria-valuemin="0" 
                    aria-valuemax="100"
                    >
                    {{this.userRankScore}}
                  </div>  
                </div>
                <span class="aladin" style="font-size: 20px;">
                  Your rank is now below -100, therefore your account has been disabled!<br> Please contact support.
                </span>
            </div>
          </div>
        </div>
<!--        <ul>-->
<!--          <li>-->
<!--            <h4 class="my-courses">My Courses:</h4>-->
<!--          </li>-->
<!--          <h4 v-if="userCourses.length === 0">No courses yet</h4>-->
<!--          <li v-else v-for="course in userCourses" :key="course">-->
<!--            &#127891; {{ course.replace("_", " - ") }}-->
<!--          </li>-->
<!--        </ul>-->
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
      // userCourses: [],
      userRankScore: 0,
      rankMap: {
        0 : "Freshman",
        1 : "Junior",
        2 : "Senior",
      },
      progressBarMin: 0,
      progressBarMax: 0
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
          this.userRankScore = data["rankScore"];
          // this.userCourses = data["courses"];
          if(data["rank"] == 0) {
            this.progressBarMax = 100
          }
          if(data["rank"] == 1) {
            this.progressBarMin = 100
            this.progressBarMax = 300
          }
          if(data["rank"] == 2) {
            this.progressBarMin = 300
            this.progressBarMax = 1000
          }
        })
        
    },
    getStyleForProgessBar() {
      return "width: "+ this.getNormalizedRank() + "%;"
    },
    getNormalizedRank() { 
      if(this.userRankScore > 1000) {
        this.userRankScore = 1000
      }
      
      const x = Math.round((this.userRankScore - this.progressBarMin) / (this.progressBarMax - this.progressBarMin) * 100)
      return x
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
  font-size: 1.3em;
  position: relative;
  display: inline-block;
  left: 50%;
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  border-radius: 30px 30px 30px 30px;
}

img {
  object-fit: cover;
  border: 1px solid #ddd;
  border-radius: 50%;
  padding: 5px;
  display: block;
  margin-bottom: 1.8em;
  margin-top: 0.5em;
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