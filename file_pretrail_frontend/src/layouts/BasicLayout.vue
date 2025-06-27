<template>
  <div id="basic-layout">
    <a-layout>
      <a-layout-header class="header">
        <GlobalHeader_user />
      </a-layout-header>
      <a-layout-content class="content">
        <router-view />
      </a-layout-content>
      <a-layout-footer class="footer">
        <a href="https://www.baidu.com" target="_blank">
          文件预审系统 by ckc
        </a>
      </a-layout-footer>
    </a-layout>
  </div>
</template>

<script setup lang="ts">
import GlobalHeader from "@/components/GlobalHeader.vue";
import { getCurrentUser } from "@/api/user";
import GlobalHeader_user from "@/components/GlobalHeader_user.vue";

getCurrentUser().then((res) => {
  console.log(res);
});
</script>

<style scoped>
#basic-layout .footer {
  background-color: #efefef;
  text-align: center;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 16px;
}

#basic-layout .content {
  padding: 20px;
  margin-bottom: 20px;
  background: linear-gradient(to right, #fefefe, #fff);
}

#basic-layout .header {
  background: white;
  margin-bottom: 16px;
  color: unset;
  padding-inline-start: 50px;
}
</style>
