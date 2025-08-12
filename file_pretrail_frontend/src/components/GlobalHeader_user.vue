<template>
  <div id="globalHeader">
    <a-row :wrap="false" justify="space-between">
      <a-col flex="200px" justify="space-between">
        <div class="title-bar">
          <img class="logo" src="../assets/title-logo.jpg" alt="logo"/>
          <div class="title">文件预审系统</div>
        </div>
      </a-col>
      <a-col flex="1" class="menu-container">
        <a-menu
            v-model:selectedKeys="current"
            mode="horizontal"
            :items="items"
            @click="doMenuClick"
        />
      </a-col>
      <a-col flex="200px" class="right-section">
        <div class="info-bar">
          <span v-if="!loginUserStore.loginUser.id" class="capsule">未登录</span>
          <span v-else>
            {{ loginUserStore.loginUser.username ?? "无名" }}
            <span v-if="loginUserStore.loginUser.userRole === 1">客户</span>
            <span v-else-if="loginUserStore.loginUser.userRole === 2">律师</span>
          </span>
        </div>
        <div class="user-login-status">
          <div v-if="!loginUserStore.loginUser.id">
            <a-button type="primary" @click="router.push('/login')">登录</a-button>
            <el-button type="primary" class="register-button" @click="router.push('/register')" plain>注册</el-button> <!-- 新增注册按钮 -->
          </div>
          <div v-else>
            <a-button type="primary" @click="router.push('/homePage')">退出</a-button>
          </div>
        </div>
      </a-col>
    </a-row>
  </div>
</template>

<script lang="ts" setup>
import {h, onMounted, ref, watch} from "vue";
import {
  MailOutlined,
  AppstoreOutlined,
  SettingOutlined,
  FileOutlined,
  UnorderedListOutlined,
  UserOutlined,
} from "@ant-design/icons-vue";
import {MenuProps} from "ant-design-vue";
import {useRouter} from "vue-router";
import {useLoginUserStore} from "@/store/useLoginUserStore";

const loginUserStore = useLoginUserStore();

const router = useRouter();

// 点击菜单后的路由跳转事件
const doMenuClick = ({key}: { key: string }) => {
  router.push({
    path: key,
  });
};

const current = ref<string[]>(["mail"]);

// 监听路由变化，更新当前菜单选中状态
router.afterEach((to, from, failure) => {
  current.value = [to.path];
});

// 根据用户身份确定菜单列表
const generateItems = (): MenuProps["items"] => {
  if (loginUserStore.loginUser && loginUserStore.loginUser.userRole === 1) {
    return [
      {
        key: "jobManagement", // Add a unique key for the parent menu
        label: "工单管理", // 父菜单没有 key
        icon: () => h(UnorderedListOutlined),
        children: [
          {
            key: "/JobManage",
            icon: () => h(FileOutlined),
            label: "已建工单",
            title: "已建工单",
          },
          {
            key: "/NewJobListForClient",
            icon: () => h(FileOutlined),
            label: "工单列表（已接）",
            title: "工单列表（已接）",
          },
        ],
      },
      {
        key: "/JobCreate",
        icon: () => h(FileOutlined),
        label: "工单创建",
        title: "工单创建",
      },
      {
        key: "/orderList",
        icon: () => h(UnorderedListOutlined),
        label: "订单管理",
        title: "订单管理",
      },
      {
        key: "lawyerList",
        icon: () => h(UnorderedListOutlined),
        label: "律师列表",
        title: "律师列表",
      },
      {
        key: "/userInfo",
        icon: () => h(SettingOutlined),
        label: "个人信息",
        title: "个人信息",
      },
    ];
  } else if (
      loginUserStore.loginUser &&
      loginUserStore.loginUser.userRole === 2
  ) {
    return [
      {
        key: "/jobList",
        icon: () => h(UnorderedListOutlined),
        label: "工单列表",
        title: "工单列表",
      },
      {
        key: "/jobListForAccept",
        icon: () => h(UnorderedListOutlined),
        label: "工单列表(已确认)",
        title: "工单详情(已确认)",
      },
      {
        key: "/orderList_Lawyer",
        icon: () => h(UnorderedListOutlined),
        label: "订单管理",
        title: "订单管理",
      },
      {
        key: "/userInfoLawyer",
        icon: () => h(SettingOutlined),
        label: "个人信息",
        title: "个人信息",
      },
    ];
  } else {
    // 未登录用户或其他情况的默认菜单
    return [
      {
        key: "/",
        icon: () => h(MailOutlined),
        label: "主页",
        title: "主页",
      },
    ];
  }
};

const items = ref<MenuProps["items"]>(generateItems());

// 监听 loginUserStore.loginUser 的变化
watch(
    () => loginUserStore.loginUser,
    () => {
      items.value = generateItems();
    },
    {deep: true}
);
</script>

<style scoped>

#globalHeader {
  margin: 0 auto; /* Center the header */
  max-width: 1200px; /* Limit the maximum width */
  padding: 0 20px; /* Add margin on both sides */
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

.menu-container {
  display: flex;
  justify-content: center; /* Center the menu horizontally */
  align-items: center; /* Center the menu vertically */
}

.logo {
  height: 48px;
}

.menu-container {
  display: flex;
  justify-content: center; /* Center the menu horizontally */
  align-items: center; /* Center the menu vertically */
  flex: 1; /* Allow the menu to take up all available space */
  overflow: visible; /* Ensure no content is hidden */
}

.left-section,
.right-section {
  display: flex;
  align-items: center;
}

.info-bar {
  margin-right: 10px; /* Keep some spacing from the button */
  display: flex;
  align-items: center;
}

.register-button {
  margin-left: 10px; /* 设置“注册”按钮与“登录”按钮的间距 */
}

.capsule {
  background-color: #fff;
  border-radius: 15px;
  padding: 0px 8px; /* Further adjusted padding */
  color: #666;
  font-size: 12px; /* Further adjusted font size */
}

</style>
