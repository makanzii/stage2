<template>
  <header>
    <div class="menu-demo">
      <a-menu mode="horizontal" :default-selected-keys="[current]" style="width: 50%">
        <a-menu-item>
          <img class="logo" src="@/assets/logomini.svg" alt="E-Class logo"/>
        </a-menu-item>
        <a-menu-item @click="navigate(item.link)" v-for="item in navigations" :key="item.name">
          {{ item.name }}
        </a-menu-item>
      </a-menu>
      <div class="search-input">
        <input v-model="keyword" @keydown.enter="search" placeholder="search questions"/>
      </div>

      <div class="userinfo">
        <a-avatar><img :src="user.avatar"/></a-avatar>
        <router-link to="/profile" class="ms-3 small">Profile</router-link>
        <a-link @click="logout" class="ms-3">Logout</a-link>
      </div>
    </div>
    <a-divider :margin="5"></a-divider>
  </header>
</template>


<script>
import server from "@/utils/api";

export default {
  data() {
    return {
      keyword: '',
      username: 'user',
      user: {},
      current: '',
      navigations: [
        {
          name: 'Dashboard',
          link: '/'
        },
        {
          name: 'Courses',
          link: '/courses'
        },
        {
          name: 'Discuss',
          link: '/discuss'
        },
        {
          name: 'Assistant',
          link: '/assistant'
        }
      ]
    }
  },
  methods: {
    navigate(path) {
      this.$router.push(path)
      this.keyword = ''
      this.current = this.navigations.find(item => item.link === path).name
    },
    search() {
      window.location.href = `/search?q=${this.keyword}`
    },
    logout() {
      localStorage.clear()
      this.$router.push('/login')
    }
  },
  mounted() {
    this.keyword = this.$route.query.q
    const user = localStorage.getItem('user')
    if (user !== undefined) {
      this.user = JSON.parse(user)
    } else {
      server.getUserInfo().then(data => {
        localStorage.setItem('user', JSON.stringify(data.data));
          this.user= data.data
      })
    }

  }
};
</script>

<style scoped>
.menu-demo {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  position: relative;
}

.search-input {
  position: absolute;
  left: 50%;
  transform: translateX(-50%) translateY(-50%);
  top: 50%;
  display: flex;
  width: 500px;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}

.search-input input {
  height: 40px;
  width: 100%;
  border-radius: 20px;
  padding-left: 20px;
  border: none;
  background-color: #ebedef;
  text-align: center;
}

.search-input input:focus {
  outline: none;
}

.userinfo {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
  padding-right: 30px;
  width: 33%;
}
a{
  text-decoration: none;
}
</style>
