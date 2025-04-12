(function(){"use strict";var e={2131:function(e,t,o){var n=o(3751),s=o(641);function a(e,t){const o=(0,s.g2)("router-view");return(0,s.uX)(),(0,s.Wv)(o)}var r=o(6262);const i={},l=(0,r.A)(i,[["render",a]]);var c=l,u=o(5220);const d={class:"login-container"},p={class:"login-box"},k={class:"form-group"},b={class:"form-group"},g={class:"additional-links"};function f(e,t,o,a,r,i){return(0,s.uX)(),(0,s.CE)("div",d,[(0,s.Lk)("div",p,[t[8]||(t[8]=(0,s.Lk)("h1",null,"Welcome Back!",-1)),t[9]||(t[9]=(0,s.Lk)("p",null,"Please log in to continue to your learning journey.",-1)),(0,s.Lk)("form",{onSubmit:t[2]||(t[2]=(0,n.D$)(((...e)=>i.login&&i.login(...e)),["prevent"]))},[(0,s.Lk)("div",k,[t[4]||(t[4]=(0,s.Lk)("label",{for:"email"},"Email",-1)),(0,s.bo)((0,s.Lk)("input",{"onUpdate:modelValue":t[0]||(t[0]=e=>r.email=e),type:"email",id:"email",placeholder:"Enter your email",required:""},null,512),[[n.Jo,r.email]])]),(0,s.Lk)("div",b,[t[5]||(t[5]=(0,s.Lk)("label",{for:"password"},"Password",-1)),(0,s.bo)((0,s.Lk)("input",{"onUpdate:modelValue":t[1]||(t[1]=e=>r.password=e),type:"password",id:"password",placeholder:"Enter your password",required:""},null,512),[[n.Jo,r.password]])]),t[6]||(t[6]=(0,s.Lk)("button",{class:"login-button",type:"submit"},"Log In",-1))],32),(0,s.Lk)("div",g,[(0,s.Lk)("p",null,[t[7]||(t[7]=(0,s.eW)("Don't have an account? ")),(0,s.Lk)("button",{onClick:t[3]||(t[3]=(...e)=>i.goToSignUp&&i.goToSignUp(...e)),class:"link-button"},"Sign Up")])])])])}o(4114);var h=o(7031),m=o(223);const v={apiKey:"AIzaSyAovTx7PHPOcl0TFsYblR3PvyKA1VCss-Y",authDomain:"adaptivelearning-ff09f.firebaseapp.com",databaseURL:"https://adaptivelearning-ff09f-default-rtdb.europe-west1.firebasedatabase.app",projectId:"adaptivelearning-ff09f",storageBucket:"adaptivelearning-ff09f.firebasestorage.app",messagingSenderId:"304947427733",appId:"1:304947427733:web:1d52843cf21a9646245e9c",measurementId:"G-L1LCPLNPRK"},y=(0,m.Wp)(v);var L=y,w={name:"UserLogin",data(){return{email:"",password:""}},methods:{async login(){const e=(0,h.xI)(L);try{const t=await(0,h.x9)(e,this.email,this.password);console.log("User logged in:",t.user),this.$router.push("/quiz")}catch(t){console.error("Login error:",t.message),alert("Login failed: "+t.message)}},goToSignUp(){this.$router.push("/signup")}}};const C=(0,r.A)(w,[["render",f],["__scopeId","data-v-79a57352"]]);var S=C,_=o(33);const O={class:"quiz-container"},E={class:"header"},q={class:"header-buttons"},T={class:"streak-container"},P={class:"streak-badge"},U={key:0,class:"loading"},F={key:1,class:"error"},j={key:2},I={class:"question"},X={class:"options"},A=["onClick","disabled"],Q={key:1,class:"feedback-buttons"},x={class:"feedback-buttons-group"};function D(e,t,o,n,a,r){return(0,s.uX)(),(0,s.CE)("div",O,[(0,s.Lk)("div",E,[t[10]||(t[10]=(0,s.Lk)("h1",{class:"title"},"Math Quiz",-1)),(0,s.Lk)("div",q,[(0,s.Lk)("button",{class:"stats-btn",onClick:t[0]||(t[0]=(...e)=>r.goToStatistics&&r.goToStatistics(...e))},"Statistics"),(0,s.Lk)("button",{class:"logout-btn",onClick:t[1]||(t[1]=(...e)=>r.logout&&r.logout(...e))},"Log Out")])]),(0,s.Lk)("div",T,[t[11]||(t[11]=(0,s.Lk)("p",{class:"streak-label"},"Current Streak:",-1)),(0,s.Lk)("span",P,(0,_.v_)(a.correctStreak),1)]),a.loading?((0,s.uX)(),(0,s.CE)("div",U,t[12]||(t[12]=[(0,s.Lk)("p",null,"Loading question...",-1),(0,s.Lk)("div",{class:"spinner"},null,-1)]))):a.error?((0,s.uX)(),(0,s.CE)("div",F,[(0,s.Lk)("p",null,(0,_.v_)(a.error),1),(0,s.Lk)("button",{onClick:t[2]||(t[2]=(...e)=>r.loadQuestion&&r.loadQuestion(...e)),class:"retry-btn"},"Retry")])):((0,s.uX)(),(0,s.CE)("div",j,[(0,s.Lk)("p",I,(0,_.v_)(a.questionData.question),1),(0,s.Lk)("div",X,[((0,s.uX)(!0),(0,s.CE)(s.FK,null,(0,s.pI)(a.questionData.options,((e,t)=>((0,s.uX)(),(0,s.CE)("button",{key:t,class:(0,_.C4)(["option-btn",{correct:a.selectedOption===e&&a.isCorrect,incorrect:a.selectedOption===e&&!a.isCorrect,"show-correct":null!==a.selectedOption&&e===a.questionData.answer&&!a.isCorrect}]),onClick:t=>r.checkAnswer(e),disabled:null!==a.selectedOption},(0,_.v_)(e),11,A)))),128))]),a.feedback?((0,s.uX)(),(0,s.CE)("p",{key:0,class:(0,_.C4)(["feedback",{"feedback-correct":a.isCorrect,"feedback-incorrect":!a.isCorrect}])},(0,_.v_)(a.feedback),3)):(0,s.Q3)("",!0),null===a.selectedOption||a.feedbackSubmitted?(0,s.Q3)("",!0):((0,s.uX)(),(0,s.CE)("div",Q,[t[13]||(t[13]=(0,s.Lk)("p",{class:"feedback-title"},"How would you rate the question's difficulty?",-1)),(0,s.Lk)("div",x,[(0,s.Lk)("button",{class:"feedback-btn",onClick:t[3]||(t[3]=e=>r.submitFeedback("Very Easy"))},"Very Easy"),(0,s.Lk)("button",{class:"feedback-btn",onClick:t[4]||(t[4]=e=>r.submitFeedback("Easy"))},"Easy"),(0,s.Lk)("button",{class:"feedback-btn",onClick:t[5]||(t[5]=e=>r.submitFeedback("Medium"))},"Medium"),(0,s.Lk)("button",{class:"feedback-btn",onClick:t[6]||(t[6]=e=>r.submitFeedback("Hard"))},"Hard"),(0,s.Lk)("button",{class:"feedback-btn",onClick:t[7]||(t[7]=e=>r.submitFeedback("Wrong"))},"Wrong"),(0,s.Lk)("button",{class:"feedback-btn skip-btn",onClick:t[8]||(t[8]=e=>r.submitFeedback("Skipped"))},"Skip")])])),a.feedbackSubmitted?((0,s.uX)(),(0,s.CE)("button",{key:2,onClick:t[9]||(t[9]=(...e)=>r.loadQuestion&&r.loadQuestion(...e)),class:"next-btn"}," Next Question ")):(0,s.Q3)("",!0)]))])}var $={name:"QuizScreen",data(){return{questionData:{question:"",options:[],answer:""},loading:!0,error:null,feedback:null,isCorrect:!1,selectedOption:null,correctStreak:0,feedbackSubmitted:!1}},methods:{async loadQuestion(){this.loading=!0,this.error=null,this.feedback=null,this.selectedOption=null,this.feedbackSubmitted=!1;try{const e=await fetch("https://adaptive-learning-489216095849.europe-west1.run.app/generate_question",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({user_id:"test_user"})});if(!e.ok)throw new Error("Failed to load question");const t=await e.json();this.questionData=t,this.correctStreak=t.correct_streak||0,this.loading=!1}catch(e){this.error="Failed to load quiz question. Please try again.",this.loading=!1}},checkAnswer(e){if(null!==this.selectedOption)return;this.selectedOption=e;const t=e.trim().toLowerCase(),o=this.questionData.answer.trim().toLowerCase();t===o?(this.isCorrect=!0,this.updateStreak(!0)):(this.isCorrect=!1,this.updateStreak(!1))},async updateStreak(e){try{const t=await fetch("https://adaptive-learning-489216095849.europe-west1.run.app/submit_answer",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({user_id:"test_user",is_correct:e})}),o=await t.json();this.correctStreak=o.correct_streak||0}catch(t){console.error("Failed to update streak:",t)}},async submitFeedback(e){try{await fetch("https://adaptive-learning-489216095849.europe-west1.run.app/feedback",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({user_id:"test_user",question:this.questionData.question,difficulty:e})}),this.feedbackSubmitted=!0,console.log(`Feedback '${e}' submitted successfully.`)}catch(t){console.error("Failed to submit feedback:",t)}},goToStatistics(){this.$router.push("/statistics")},logout(){console.log("User logged out"),this.$router.push("/login")}},mounted(){this.loadQuestion()}};const J=(0,r.A)($,[["render",D],["__scopeId","data-v-0fd927f8"]]);var z=J;const V={class:"progress-container"};function W(e,t,o,n,a,r){return(0,s.uX)(),(0,s.CE)("div",V,[t[0]||(t[0]=(0,s.Lk)("h1",null,"Your Progress",-1)),(0,s.Lk)("ul",null,[((0,s.uX)(!0),(0,s.CE)(s.FK,null,(0,s.pI)(a.progress,((e,t)=>((0,s.uX)(),(0,s.CE)("li",{key:t},[(0,s.Lk)("strong",null,(0,_.v_)(t)+":",1),(0,s.Lk)("p",null,"Accuracy: "+(0,_.v_)(e.accuracy)+"%",1),(0,s.Lk)("p",null,"Completed Questions: "+(0,_.v_)(e.completed_questions),1)])))),128))])])}var K=o(4335),M={data(){return{progress:{}}},async mounted(){await this.fetchProgress()},methods:{async fetchProgress(){try{const e=await K.A.get("http://localhost:5000/users/test_user_1/progress");this.progress=e.data}catch(e){console.error("Error fetching progress:",e)}}}};const N=(0,r.A)(M,[["render",W],["__scopeId","data-v-54bf06a4"]]);var R=N;const H={class:"signup-container"};function Y(e,t,o,a,r,i){return(0,s.uX)(),(0,s.CE)("div",H,[t[7]||(t[7]=(0,s.Lk)("h1",null,"Sign Up",-1)),(0,s.Lk)("form",{onSubmit:t[2]||(t[2]=(0,n.D$)(((...e)=>i.signUp&&i.signUp(...e)),["prevent"]))},[t[4]||(t[4]=(0,s.Lk)("label",{for:"email"},"Email:",-1)),(0,s.bo)((0,s.Lk)("input",{type:"email","onUpdate:modelValue":t[0]||(t[0]=e=>r.email=e),id:"email",required:""},null,512),[[n.Jo,r.email]]),t[5]||(t[5]=(0,s.Lk)("label",{for:"password"},"Password:",-1)),(0,s.bo)((0,s.Lk)("input",{type:"password","onUpdate:modelValue":t[1]||(t[1]=e=>r.password=e),id:"password",required:""},null,512),[[n.Jo,r.password]]),t[6]||(t[6]=(0,s.Lk)("button",{type:"submit"},"Sign Up",-1))],32),(0,s.Lk)("button",{onClick:t[3]||(t[3]=(...e)=>i.goToLogin&&i.goToLogin(...e)),class:"login-button"},"Back to Login")])}var B={data(){return{email:"",password:""}},methods:{async signUp(){const e=(0,h.xI)(L);try{const t=await(0,h.eJ)(e,this.email,this.password);console.log("User signed up:",t.user),alert("Sign up successful! You can now log in."),this.$router.push("/login")}catch(t){console.error("Sign up error:",t.message),alert("Sign up failed: "+t.message)}},goToLogin(){this.$router.push("/login")}}};const G=(0,r.A)(B,[["render",Y],["__scopeId","data-v-4665f636"]]);var Z=G;const ee=[{path:"/",redirect:"/login"},{path:"/login",component:S},{path:"/quiz",component:z},{path:"/progress",component:R},{path:"/signup",component:Z}],te=(0,u.aE)({history:(0,u.LA)(),routes:ee});var oe=te,ne=o(6278),se=(0,ne.y$)({state:{},getters:{},mutations:{},actions:{},modules:{}});const ae="https://adaptive-learning-489216095849.europe-west1.run.app";window.API_URL=ae,(0,n.Ef)(c).use(se).use(oe).mount("#app")}},t={};function o(n){var s=t[n];if(void 0!==s)return s.exports;var a=t[n]={exports:{}};return e[n].call(a.exports,a,a.exports,o),a.exports}o.m=e,function(){var e=[];o.O=function(t,n,s,a){if(!n){var r=1/0;for(u=0;u<e.length;u++){n=e[u][0],s=e[u][1],a=e[u][2];for(var i=!0,l=0;l<n.length;l++)(!1&a||r>=a)&&Object.keys(o.O).every((function(e){return o.O[e](n[l])}))?n.splice(l--,1):(i=!1,a<r&&(r=a));if(i){e.splice(u--,1);var c=s();void 0!==c&&(t=c)}}return t}a=a||0;for(var u=e.length;u>0&&e[u-1][2]>a;u--)e[u]=e[u-1];e[u]=[n,s,a]}}(),function(){o.d=function(e,t){for(var n in t)o.o(t,n)&&!o.o(e,n)&&Object.defineProperty(e,n,{enumerable:!0,get:t[n]})}}(),function(){o.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){o.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)}}(),function(){o.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})}}(),function(){var e={524:0};o.O.j=function(t){return 0===e[t]};var t=function(t,n){var s,a,r=n[0],i=n[1],l=n[2],c=0;if(r.some((function(t){return 0!==e[t]}))){for(s in i)o.o(i,s)&&(o.m[s]=i[s]);if(l)var u=l(o)}for(t&&t(n);c<r.length;c++)a=r[c],o.o(e,a)&&e[a]&&e[a][0](),e[a]=0;return o.O(u)},n=self["webpackChunkadaptive_learning_frontend"]=self["webpackChunkadaptive_learning_frontend"]||[];n.forEach(t.bind(null,0)),n.push=t.bind(null,n.push.bind(n))}();var n=o.O(void 0,[504],(function(){return o(2131)}));n=o.O(n)})();
//# sourceMappingURL=app.ef29f4e8.js.map