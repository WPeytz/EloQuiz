import { createStore } from 'vuex'

export default createStore({
  state: {
    user:null
  },
  getters: {
    getUser: state => state.user
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    }
  },
  actions: {
    setUser({ commit }, user) {
      commit('setUser', user);
    }
  },
  modules: {
  }
})
