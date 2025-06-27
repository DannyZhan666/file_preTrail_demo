import myAxios from "@/request";

export const fileUpload = async (params: any) => {
  return await myAxios.request({
    url: "/file/upload",
    method: "POST",
    data: params,
  });
};

export const filePage = async (page = 1, pageSize = 10) => {
  return await myAxios.request({
    url: "/file/pageByUser",
    method: "GET",
    params: {
      page: page,
      pageSize: pageSize,
    },
  });
};
