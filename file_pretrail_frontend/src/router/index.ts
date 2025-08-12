import {createRouter, createWebHashHistory, RouteRecordRaw} from "vue-router";
import HomePage from "@/pages/HomePage.vue";
import userLogin from "@/pages/user/userLogin.vue";
import userRegisterPage from "@/pages/user/userRegisterPage.vue";
import LawyerHome from "@/pages/lawyer/LawyerHome.vue";
import JobList from "@/pages/lawyer/JobList.vue";
import UserInfo_lawyer from "@/pages/lawyer/UserInfo_lawyer.vue";
import OrderList_lawyer from "@/pages/lawyer/OrderList_lawyer.vue";
import JobDetails from "@/pages/lawyer/JobDetails.vue";
import GlobalHeader_user from "@/components/GlobalHeader_user.vue";
import homeHeader from "@/components/homeHeader.vue";
import BasicLayout from "@/layouts/BasicLayout.vue";
import JobManage from "@/pages/client/JobManage.vue";
import LawyerList from "@/pages/client/LawyerList.vue";
import OrderList from "@/pages/client/OrderList.vue";
import UserInfo from "@/pages/client/UserInfo.vue";
import JobCreate from "@/pages/client/JobCreate.vue";
import NewJobListForClient from "@/pages/client/NewJobListForClient.vue";
import JobDetailsClientAccept from "@/pages/client/JobDetails_client_accept.vue";
import JobListForAccept from "@/pages/lawyer/JobListForAccept.vue";
import JobDetailsForAccept from "@/pages/lawyer/JobDetailsForAccept.vue";
import OrderDetails_client from "@/pages/client/orderDetails_client.vue";
import JobDetails_client_origin from "@/pages/client/JobDetails_client_origin.vue";
import JobDetails_client_accept from "@/pages/client/JobDetails_client_accept.vue";

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        redirect: 'homePage',
    },
    {
        path: '/homePage',
        meta: {title: "首页"},
        component: HomePage
    },
    {
        path: '/login',
        meta: {title: "登录"},
        component: userLogin
    },
    {
        path: '/register',
        meta: {title: "注册"},
        component: userRegisterPage
    },
    {
        path: '/user',
        component: BasicLayout,
        redirect: '/JobManage',
        children: [
            // {
            //   path: '/uploadFile',
            //   meta: {title: "文件上传"},
            //   component: UploadFile
            // },
            {
                path: '/jobManage',
                meta: {title: "已建工单"},
                component: JobManage
            },
            {
                path: '/jobCreate',
                meta: {title: "工单创建"},
                component: JobCreate
            },
            {
                path: '/NewJobListForClient',
                meta: {title: "工单列表（已接）"},
                component: NewJobListForClient
            },
            {
                path: '/lawyerList',
                meta: {title: "律师列表"},
                component: LawyerList
            },
            {
                path: '/JobDetails_client_origin/:id?',
                name: 'JobDetails_client_origin',
                meta: {title: "工单详情"},
                component: JobDetails_client_origin
            },
            {
                path: '/JobDetails_client_accept/:id?',
                name: 'JobDetails_client_accept',
                meta: {title: "工单详情（已接）"},
                component: JobDetails_client_accept
            },
            {
                path: '/orderList',
                meta: {title: "订单管理"},
                component: OrderList
            },
            {
                path: '/orderDetails_client/:id?',
                name: 'orderDetails_client',
                meta: {title: "订单详情"},
                component: OrderDetails_client
            },
            {
                path: '/userInfo',
                meta: {title: "个人信息"},
                component: UserInfo
            },
        ]
    },
    // 律师页面
    {
        path: '/lawyer',
        component: BasicLayout,
        redirect: '/jobList',
        children: [
            {
                path: '/jobList',
                meta: {title: "工单列表"},
                component: JobList
            },
            {
                path: '/jobDetails/:id?',
                name: 'jobDetails',
                meta: {title: "工单详情"},
                component: JobDetails
            },
            {
                path: '/jobListForAccept',
                meta: {title: "工单列表"},
                component: JobListForAccept
            },
            {
                path: '/jobDetailsForAccept/:id?',
                name: 'jobDetailsForAccept',
                meta: {title: "工单详情"},
                component: JobDetailsForAccept
            },
            {
                path: '/orderList_lawyer',
                meta: {title: "订单管理"},
                component: OrderList_lawyer
            },
            {
                path: '/userInfoLawyer',
                meta: {title: "个人信息"},
                component: UserInfo_lawyer
            },
        ]
    },
    ///////////
];

const router = createRouter({
    history: createWebHashHistory(process.env.BASE_URL),
    routes,
});

export default router;
