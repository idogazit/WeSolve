<template>
  <div id="app">
    <NavbarComponent/>
    <Breadcrumb :crumbs="crumbs" @selected="selected" />
    <SelectNext :links="links" :level="level[crumbs.length]" @selectedLink="selectedLink" />
    <router-view/>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import NavbarComponent from "@/components/Navbar.vue";
import Breadcrumb from "@/components/BreadCrumb.vue";
import SelectNext from "@/components/SelectNext.vue";
export default {
  name: "App",
  components: {
    NavbarComponent,
    Breadcrumb,
    SelectNext
  },
  data() {
    return {
      crumbs: ['TAU'],
      level: ['university', 'faculty', 'school', 'course', 'year'],
      links: links
    };
  },
  methods: {
    async setUserInfo() {
      // add the username of the logged in user to localStorage
      const data = await apiService("/api/user/");
      const requestUser = data["username"];
      window.localStorage.setItem("username", requestUser);
    },
    loadUpTAU(){
    let endpoint = "/api/nav/faculties/"
    apiService(endpoint)
        .then(data => {
          this.links = data["results"]
      })
    },
    selected(crumb, ci) {
      // TODO: need to call API to get previous setting by the crumb selected
      this.crumbs = this.crumbs.slice(0, ci + 1)
      //this.links = ['Computer Science', 'Chemistry', 'Physics']
      //console.log(crumb)
      let endpoint = "/api/nav/" + this.level[this.crumbs.length+1]+"s/?"+ this.level[this.crumbs.length] + "=" + crumb;
      apiService(endpoint)
        .then(data => {
          this.links = data["results"]
        })
    },
    selectedLink(link) {
      let endpoint = "/api/nav/" + this.level[this.crumbs.length+1]+"s/?"+ this.level[this.crumbs.length] + "=" + link;
      apiService(endpoint)
        .then(data => {
          this.links = data["results"]
        })
      this.crumbs.push(link)
    }
  },
  created() {
    this.setUserInfo()
    this.loadUpTAU()
  }
};
</script>

<style>
html,
body {
  height: 100%;
  font-family: "Playfair Display", serif;
}

.btn:focus {
  box-shadow: none !important;
}
</style>
