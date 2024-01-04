import http from "./requst";

// Get the user list
export async function getUserList(page = 1, size = 10) {
    const res = await http.get(`/get_user_list?page=${page}&size=${size}`)
    console.log('response', res)
    return res
}

// Add user
export async function postAddUser(name: string, gender: string) {
    const res = await http.post(`/add_user`, {
        name,
        gender
    })
    return res
}

export async function postEditUser(name: string, gender: string, originName: string) {
    const res = await http.post(`/edit_user`, {
        name,
        gender,
        originName
    })
    return res
}