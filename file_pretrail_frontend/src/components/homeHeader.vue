<template>
  <div id="globalHeader">
    <a-row :wrap="false">
      <a-col flex="200px">
        <div class="title-bar">
          <img class="logo" src="../assets/title-logo.jpg" alt="logo" />
          <div class="title">文件预审系统</div>
        </div>
      </a-col>
<!--      <a-col flex="auto">-->
<!--        <a-menu-->
<!--            v-model:selectedKeys="current"-->
<!--            mode="horizontal"-->
<!--            :items="items"-->
<!--            @click="doMenuClick"-->
<!--        />-->
<!--      </a-col>-->
<!--      <a-col flex="80px">-->
<!--        <div class="user-login-status">-->
<!--          <div v-if="loginUserStore.loginUser.id">-->
<!--            {{ loginUserStore.loginUser.username ?? "无名" }}-->
<!--          </div>-->
<!--          <div v-else>-->
<!--            <a-button type="primary" @click="router.push('/login')">登录</a-button>-->
<!--          </div>-->
<!--        </div>-->
<!--      </a-col>-->
    </a-row>
  </div>
</template>

<script >
export default {
  name: 'App',
  data() {
    return {
      activeIndex: 1,
    }
  },
  methods: {
    changePage(path) {
      this.$router.push(path)
    },
    logout(){
      this.$router.push('/login');
    },
  },
}
</script>

<style scoped>
.whole {
  height: 100%;
}


.el-header, .el-footer {
  background-color: #B3C0D1;
  color: #333;
  text-align: center;
  line-height: 60px;
}

.el-aside {
  background-color: #D3DCE6;
  color: #333;
  text-align: center;
  line-height: 200px;
}

.el-menu {
  border-right: none;
}

.el-main {
  background-color: #E9EEF3;
  color: #333;
  text-align: center;
  line-height: 20px;
}

body > .el-container {
  margin-bottom: 40px;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
  line-height: 260px;
}

.el-container .el-aside {
  line-height: 320px;
}

.title-bar {
  display: flex;
  align-items: center;
}

.title {
  color: black;
  font-size: 18px;
  margin-left: 16px;
}

.logo {
  height: 48px;
}
</style>
