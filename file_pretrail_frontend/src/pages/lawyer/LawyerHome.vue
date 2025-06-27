<template>
  <div class="whole">
    <el-container>
      <el-header><div><b style="float: left;margin-top: -20px"><h2 style="color: #c09494">文件预审系统</h2></b>

        <el-button class="logout" type="warning" @click="logout">退出</el-button>
      </div></el-header>
      <el-container>
        <el-aside width="200px">
          <el-menu

            default-active="index"
            class="el-menu-vertical-demo"
            background-color="#545c64"
            text-color="#fff"
            active-text-color="#c09494">

            <el-menu-item index="/jobList" @click="changePage('/jobList')">
              <i class="el-icon-menu"></i>
              工单列表
            </el-menu-item>
            <el-menu-item index="/jobDetails" @click="changePage('/jobDetails')">
              <i class="el-icon-menu"></i>
              工单详情
            </el-menu-item>
            <el-menu-item index="/orderList_lawyer" @click="changePage('/orderList_lawyer')">
              <i class="el-icon-menu"></i>
              订单管理
            </el-menu-item>
            <el-menu-item @click="changePage('/userInfoLawyer')">
              <i class="el-icon-menu"></i>
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
