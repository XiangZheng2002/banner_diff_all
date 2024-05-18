import request from '@/utils/request'

// style, type, user_id, category
export const getMaterialList = (params) => 
    request.get('/get_files', {
        params
    })

export const getMaterialById = (params) =>
    request.get('/image', {
        params
    })

export const uploadMaterial = (user_id, params) =>
    request.post(`/upload?user_id=${user_id}`, {...params}, {type: 'form'})

export const getMaterialTag = (user_id, img_id) => 
    request.get('/tag', {params:{user_id, img_id}})