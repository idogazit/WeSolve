import Vue from "vue";
import Router from "vue-router";
import AnswerEditor from "./views/AnswerEditor.vue";
import HomeView from "./views/Home.vue";
import ProfileView from "./views/Profile.vue";
import AboutUsView from "./views/AboutUs.vue";
import ContactUsView from "./views/ContactUs.vue";
import NotFound from "./views/NotFound.vue";
import QuestionEditor from "./views/QuestionEditor.vue";


Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: "/search",
      name: "search",
      component: HomeView,
    },
    {
      path: "/profile",
      name: "profile",
      component: ProfileView
    },
    {
      path: "/",
      name: "about-us",
      component: AboutUsView,
      beforeEnter: (to, from, next) => {
        localStorage.clear();
        next();
      }
    },
    {
      path: "/contact",
      name: "contact-us",
      component: ContactUsView
    },
    {
      // the ? sign makes the slug parameter optional
      path: "/ask/:slug?",
      name: "question-editor",
      component: QuestionEditor,
      props: true
    },
    {
      path: "/answer/:id",
      name: "answer-editor",
      component: AnswerEditor,
      props: true
    },
    {
      path: "*",
      name: "page-not-found",
      component: NotFound
    }
  ]
});
