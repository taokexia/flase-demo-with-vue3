import axios from "axios"

const http = axios.create({
    baseURL: 'http://127.0.0.1:8080/v1',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json'
    }
})

http.interceptors.response.use(response => {
    return response.data;
});


export default http;