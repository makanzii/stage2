<script>
import server from "@/utils/api";

export default {
  data() {
    return {
      formData: {
        username: '',
        email: '',
        password: '',
      }
    };
  },
  methods: {
    handleRegister() {
      server.register(this.formData).then((res) => {
        console.log(res);
        this.$message.success('Register success!');
        this.$router.push({name: "Login"});
      }).catch((err) => {
        this.$message.error(err.response.data.error);
      });
    }
  },
  mounted() {
  },
};
</script>

<template>
  <main>
    <div class="logo-bg">
      <img class="logo" src="@/assets/logo.svg" alt="E-Class logo"/>
    </div>

    <div class="authentication">
      <h2>Sign up</h2>
      <a-form layout="vertical" :model="formData" :style="{ width: '600px' }" @submit="handleRegister">
        <a-form-item field="email" label="Email">
          <a-input
              v-model="formData.email"
              size="large"
              placeholder="please enter your email..."
          />
        </a-form-item>
        <a-form-item field="username" label="Username">
          <a-input
              v-model="formData.username"
              size="large"
              placeholder="please enter your username..."
          />
        </a-form-item>
        <a-form-item field="password" label="password">
          <a-input type="password" size="large" v-model="formData.password"
                   placeholder="please enter your password..."/>
        </a-form-item>
        <a-form-item>
          <a-button html-type="submit">Submit</a-button>
        </a-form-item>
      </a-form>

      <div class="signup">
        <span>Already have an account?</span>
        <a-link href="/login">login</a-link>
      </div>
    </div>
  </main>
</template>

<style scoped>
main {
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}

.logo-bg {
  background-color: lightcyan;
  width: 48%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.authentication {
  width: 48%;
}
</style>
