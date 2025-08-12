<template>
  <div class="whole">
    <el-container>
      <el-header>
        <div><b style="float: left;margin-top: -20px"><h2 style="color: #d79797">文件预审系统</h2></b>
          <el-button class="logout" type="warning" @click="logout">退出</el-button>
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <el-menu
            router
            :default-active="defaultUrl"
            class="el-menu-vertical-demo"
            background-color="#545c64"
            text-color="#fff"
            active-text-color="#d79797"
          >

<!--            <el-menu-item index="uploadFile">-->
<!--              <i class="el-icon-menu"></i>-->
<!--              文件上传-->
<!--            </el-menu-item>-->

            <el-menu-item index="jobManage">
              <i class="el-icon-document"></i>
              <span>工单管理</span>
            </el-menu-item>

            <el-menu-item index="lawyerList">
              <i class="el-icon-document"></i>
              <span>律师列表</span>
            </el-menu-item>

            <el-menu-item index="JobDetails_client_accept">
              <i class="el-icon-document"></i>
              <span>工单详情</span>
            </el-menu-item>

            <el-menu-item index="orderList">
              <i class="el-icon-document"></i>
              <span>订单管理</span>
            </el-menu-item>

            <el-menu-item index="userInfo">
              <i class="el-icon-document"></i>
              <span>个人信息</span>
            </el-menu-item>

          </el-menu>
        </el-aside>
        <el-container>
          <!--     主体区域     -->
          <el-main>
            <router-view></router-view>
          </el-main>
        </el-container>
      </el-container>

    </el-container>


  </div>
</template>

<script>
  export default {
    data() {
      return {
        activeIndex: 1,
        defaultUrl: 'goods',
      }
    },
    // 监听路由变化
    watch: {
      '$route': 'getPath'
    },
    methods: {
      getPath() {
        this.defaultUrl = this.$route.path.replace('/', '');
        console.log(this.defaultUrl)
      },
      changePage(path) {
        this.$router.push(path)
      },
      logout() {
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

  .my-menu {
    position: absolute;
    margin-top: 10px;
    margin-left: 10px;
  }

  .main {
    height: 80%;
  }

  .el-container {
    height: 100%;
  }

  .el-header {
    background-color: #ffffff;
  }

  .el-aside {
    height: 100%;
    background-color: #545c64;
  }

  .el-main {
    background-color: #efe8e8;
  }

  .menu-child-item {
    margin-left: 20px;
  }

  .el-footer {
    background-color: cornflowerblue;
  }

  .welcome {
    float: left;

    color: cornflowerblue;
  }
</style>
