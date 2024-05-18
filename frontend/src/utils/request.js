// 封装axios
import axios from 'axios';
import router from '@/router';
import qs from 'qs';

let _toast = null;

function setToast(t) {
    _toast = t;
}

function toastErr(msg) {
    if (!_toast)
        return;

    _toast.add({
        life: 5000,
        severity: "error",
        summary: "获取错误",
        detail: msg
    });
}

const baseURL = '/api';

const instance = axios.create({
    baseURL,
    timeout: 5000
});

// 添加请求拦截器
instance.interceptors.request.use(
    (config) => {
        config.headers['Content-Type'] = 'application/json'
        // 一般都是application/json
        // 但是也有部分接口需要传递的是formData格式的
        // 此时用到qs，为了做区分，在config参数中添加一个type变量来进行判断处理
        if (config.type && config.type === 'form') {
            config.headers['Content-Type'] = 'multipart/form-data'
            if (config.data) {
                config.data = qs.stringify(config.data);
            }
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    })

// 添加响应拦截器
instance.interceptors.response.use(
    (response) => {
        const code = response.data.code
        if (code < 200 || code > 300) {
            if (code === 401) {
                toastErr("请先登录.");
                router.push("/login");
            } else if (code === 403) {
                toastErr("权限不足.");
            } else if (code >= 500) {
                toastErr("服务器内部错误.");
            }
            Promise.reject(response.data)
        } else {
            return response.data
        }
    },
    (error) => {
        if (error.response.code === 401) {
            // 这里应该带一个redirect，待修
            router.push('/login');
        }
        // 错误的默认情况
        toastErr(error.response.data.message || '服务异常');
        console.log(error.response.data.message || '服务异常');
        return Promise.reject(error)
    })

export default instance

export {baseURL, setToast}