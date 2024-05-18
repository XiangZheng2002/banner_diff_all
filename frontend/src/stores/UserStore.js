import axios from 'axios';
import {defineStore} from "pinia";
import {ref, computed, watch} from "vue";

const useUserStore = defineStore("user", () => {
    const _userid = ref(null);
    const _username = ref(null);
    const _avatar = ref(null);
    const _isAdmin = ref(false);

    const _isAuthed = ref(false);

    const _login = axios.create({
        baseURL: '/api/login', method: 'post', headers: {
            'Content-Type': 'application/json'
        }
    });

    const _logout = axios.create({
        baseURL: '/api/logout', method: 'get', headers: {
            'Content-Type': 'application/json'
        }
    });

    /**
     * @brief 用户登录方法
     *
     * @param username string, 用户名.
     * @param pwd string, 目前是密码明文. 未来可能换成某种哈希(?)
     * @param isAdmin boolean, 是否是管理员
     * @param cb function(status: int, msg: string), 回调函数. 我们约定成功的时候status为0, 否则为1.
     */
    function login(username, pwd, isAdmin, cb) {
        _login.post('', {
            username: username, password: pwd, is_admin: isAdmin.toString()
        }).then(res => {
            if (res.data.code === 200) {
                let d = res.data.data;

                _userid.value = d.user_id;
                _username.value = username
                _avatar.value = d.avatar_url;
                _isAdmin.value = d.is_admin;

                _isAuthed.value = true;
                cb(0, res.data.message);
            } else {
                _isAuthed.value = false;
                cb(1, res.data.message);
            }
        }).catch((err) => {
            cb(1, err.message);
        });
    }

    /**
     * @brief 用户登出方法
     * @param cb function(status: int, msg: string), 回调函数. 约定同上.
     */
    function logout(cb) {
        _logout.get('').then(res => {
            if (res.data.code === 200) {
                _isAuthed.value = false;
                cb(0, res.data.message);
            } else {
                cb(1, res.data.message);
            }
        }).catch((err) => {
            cb(1, err.message);
        });
    }

    /**
     * @brief 用户是否已经登录
     * @type {ComputedRef<boolean>}
     */
    const isAuthed = computed(() => _isAuthed.value);

    /**
     * @brief 用户是否是管理员
     * @type {ComputedRef<boolean>}
     */
    const isAdmin = computed(() => _isAdmin.value);

    /**
     * @brief 获取用户信息, 是用户id, 用户名, 头像url的元组。若未登录则返回null.
     * @type {ComputedRef<null|{avatar: null extends ShallowRef<infer V> ? V : (null extends Ref<infer V> ? UnwrapRefSimple<V> : UnwrapRefSimple<null>), userid: null extends ShallowRef<infer V> ? V : (null extends Ref<infer V> ? UnwrapRefSimple<V> : UnwrapRefSimple<null>), username: null extends ShallowRef<infer V> ? V : (null extends Ref<infer V> ? UnwrapRefSimple<V> : UnwrapRefSimple<null>)}>}
     */
    const getUserInfo = computed(() => {
        if (!_isAuthed.value) {
            return null;
        }

        return {
            userid: _userid.value, username: _username.value, avatar: _avatar.value
        };
    });

    return {
        _userid, _username, _avatar, _isAdmin, _isAuthed,

        login, logout, isAuthed, isAdmin, getUserInfo
    };
});

export default useUserStore;