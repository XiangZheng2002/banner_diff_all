import request from '@/utils/request'

export const getDraftInfo = (params) => 
    request.get('/project', {
        params
    })

export const saveDraftInfo = (user_id, project_id, params) => 
    request.post(`/save?user_id=${user_id}&project_id=${project_id}`, {
        ...params
    })

export const gernerateDraft = (user_id, project_id,result_count) => 
    request.post(`/process?user_id=${user_id}&project_id=${project_id}&result_count=${result_count}`, {})