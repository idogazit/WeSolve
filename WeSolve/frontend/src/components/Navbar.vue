<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light my-navbar">
    <div class="container">
      <router-link 
        :to="{ name: 'about-us' }" 
        class="navbar-brand"
        >WeSolve
      </router-link>

      <div class="collapse navbar-collapse">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item active">
            <router-link
              :to="{ name: 'search' }" 
              class="btn btn-sm btn-info"
              >Search
            </router-link>
          </li>
          <li class="nav-item active">
            <router-link
              :to="{ name: 'profile' }"
              class="btn btn-sm btn-success"
              >Profile
            </router-link>
          </li>
          <li class="nav-item active">
            <router-link
              :to="{ name: 'about-us' }"
              class="btn btn-sm btn-success"
              >About Us
            </router-link>
          </li>
          <li class="nav-item active">
            <router-link
              :to="{ name: 'contact-us' }"
              class="btn btn-sm btn-success"
              >Contact Us
            </router-link>
          </li>
          <li class="nav-item">
            <a class="btn btn-sm btn-outline-secondary" href="/accounts/logout/"
              >Logout
            </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import {apiService} from "@/common/api.service";

export default {
  name: "NavbarComponent",
  data () {
    return {
      userInfo : null,
      isAdmin : false,
    }
  },
  methods: {
    getUserInfo() {
      let endpoint = "/api/users/current/";
      apiService(endpoint)
        .then(data => {
          this.userInfo = data;
          if (this.userInfo["username"] === "admin") {
            this.isAdmin = true;
          }
        })
    }
  },
  created() {
    this.getUserInfo()
  }
};
</script>

<style>
.my-navbar {
  border-bottom: 1px solid #ddd;
}

.navbar-brand {
  font-family: 'Aladin', cursive;
  font-weight: bold;
  font-size: 150%;
}

.navbar-brand:hover {
  color: #dc3545 !important;
}


.nav-item {
  padding: .15rem;
}
</style>