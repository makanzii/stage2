<template>
  <main class="container py-3 d-flex flex-column align-items-center">
    <div style="width: 800px">
      <div class="mb-3">
        <strong class="fs-5 ">Edit Profile</strong>
      </div>
      <a-divider/>
      <div>
        <a-form :model="form" :style="{ width: '600px' }" @submit="handleSubmit">
          <a-form-item field="avatar" label="Avatar">
            <img class="avatar" :src="form.avatar" @click="chooseAvatar"/>
            <input @change="avatarFileChange" type="file" accept="image/*" hidden id="avatarFileSelect"/>
          </a-form-item>
          <a-form-item field="email" label="Email">
            <a-input
                v-model="form.email"
                disabled
            />
          </a-form-item>
          <a-form-item field="username" label="Username">
            <a-input
                v-model="form.username"
                placeholder="please enter your new username"
            />
          </a-form-item>
          <a-form-item field="password" label="Password">
            <a-input v-model="form.password" placeholder="please enter your new password..."/>
          </a-form-item>
          <a-form-item>
            <a-button html-type="submit">Submit</a-button>
          </a-form-item>
        </a-form>
      </div>
    </div>
  </main>
</template>
<script>
import server from "@/utils/api";

export default {
  data() {
    return {
      form: {
        avatar: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxwmlnoJbzLcou6rVQAZ1_ayDmxTKBUs4WaXJ7RmVkZg&s',
        username: '',
        password: '',
      }
    }
  },
  methods: {
    chooseAvatar() {
      document.getElementById("avatarFileSelect").click();
    },
    avatarFileChange(ev) {
      const file = ev.target.files[0];
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        this.form.avatar = reader.result;
      };
    },
    handleSubmit() {
      if (this.form.username) {
        server.updateUserInfo(this.form).then(data => {
          this.$message.success("Update success!")
          localStorage.setItem('user', JSON.stringify(data.data));
          window.location.reload()
        })
      }
    },
    getUser() {
      const user = localStorage.getItem('user')
      if (user !== undefined) {
        this.form = JSON.parse(user)
      } else {
        server.getUserInfo().then(data => {
          localStorage.setItem('user', JSON.stringify(data.data));
          this.form = data.data
        })
      }
    }
  },
  mounted() {
    this.getUser()
  }
}
</script>
<style>
.avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  cursor: pointer;
}
</style>
