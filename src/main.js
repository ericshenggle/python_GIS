import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import Axios from 'axios'
import echarts from 'echarts/dist/echarts.min.js'
import 'echarts/map/js/world.js'
import china from 'echarts/map/json/china.json'

Vue.use(ElementUI)

Vue.config.productionTip = false

Axios.defaults.baseURL = 'http://127.0.0.1:8888/'
Axios.defaults.withCredentials = true
Vue.prototype.$axios = Axios
echarts.registerMap('china', china)
Vue.prototype.$echarts = echarts

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
