<script setup lang="ts">
import { onBeforeMount, reactive, ref } from 'vue'
import { getUserList, postAddUser, postEditUser } from '@/api/user'
import { showToast } from '@/utils/toast'

const data = reactive({
    list: [],
    pages: 1,
    total: 0,
    currentPage: 1,
    pageSize: 5
})
const formValue = reactive({
    name: '',
    gender: 'male'
})
const modal = ref(null)
const isAdd = ref(true)
const editUser = ref(null)

const vGender = {
    mounted: (el, binding) => {
        const value = binding.value
        if (Number(value) === 1) {
            el.textContent = 'Male'
        } else if (Number(value) === 2) {
            el.textContent = 'Female'
        } else {
            el.textContent = value
        }
    }
}

onBeforeMount(async () => {
    await fetchUserList(data.currentPage, data.pageSize)
})

const fetchUserList = async (currentPage, pageSize) => {
    const res = await getUserList(currentPage, pageSize)
    if (res.code === 1000) {
        // 请求成功
        const resData = res.data
        data.list = resData.list
        data.pages = resData.pages
        data.total = resData.total
    }
}

const addUserModal = () => {
    isAdd.value = true
    modal.value.showModal()
}

const editUserModal = (item) => {
    isAdd.value = false
    // save value for edit
    editUser.value = item
    formValue.name = item.name
    if (Number(item.gender) === 1) {
        formValue.gender = 'male'
    } else if (Number(item.gender) === 2) {
        formValue.gender = 'female'
    }
    modal.value.showModal()
}

const SubmitUserForm = async () => {
    console.log(formValue)
    if (!formValue.name) {
        showToast('Please input username!', 'error')
        return
    }

    if (isAdd.value) {
        // add User
        const res = await postAddUser(formValue.name, formValue.gender)
        console.log('response', res)
        if (res.code === 2009) {
            showToast('User already existed!')
            return
        } else if (res.code === 1000) {
            showToast('Created successfully!')
            modal.value.close()
            await fetchUserList(data.currentPage, data.pageSize)
            return
        } else {
            showToast('Created fail! Please retry.', 'error')
            return
        }
    } else {
        // edit User
        const res = await postEditUser(formValue.name, formValue.gender, editUser.value.name)
        if (res.code === 2009) {
            showToast('User already existed!')
            return
        } else if (res.code === 1000) {
            showToast('Modifiy successfully!')
            modal.value.close()
            await fetchUserList(data.currentPage, data.pageSize)
            return
        } else {
            showToast('Modify fail! Please retry.', 'error')
            return
        }
    }
}

const handleNext = async () => {
    data.currentPage = data.currentPage + 1
    await fetchUserList(data.currentPage, data.pageSize)
}
const handlePrevious = async () => {
    data.currentPage = data.currentPage - 1
    await fetchUserList(data.currentPage, data.pageSize)
}
const handlePageChange = async (page: number) => {
    data.currentPage = page
    await fetchUserList(data.currentPage, data.pageSize)
}
</script>

<template>
    <div class="flex flex-col justify-center items-center w-full h-full bg-green-50">
        <div class="container w-3/4">
            <button class="btn btn-primary" @click="addUserModal">Add User</button>
            <div class="card shadow-xl mt-10">
                <table class="table">
                    <!-- head -->
                    <thead>
                        <tr>
                            <th></th>
                            <th>Name</th>
                            <th>Gender</th>
                            <th>Operation</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- row 1 -->
                        <tr v-for="item in data.list" :key="item.uid">
                            <th>{{ item.uid }}</th>
                            <td>{{ item.name }}</td>
                            <td v-gender="item.gender"></td>
                            <td><button className="btn btn-info" @click="editUserModal(item)">Edit</button></td>
                        </tr>
                    </tbody>
                </table>
                <!-- pagination -->
                <div class="join m-2">
                    <button class="join-item btn" :class="{ 'btn-disabled': data.currentPage <= 1 }" @click="handlePrevious">«</button>
                    <button v-for="(page, index) in data.pages" :key="index" class="join-item btn"
                        :class="{ 'btn-active': data.currentPage === index + 1 }"
                        @click="handlePageChange(index + 1)">{{ index + 1 }}</button>
                    <button class="join-item btn" :class="{ 'btn-disabled': data.currentPage >= data.pages }" @click="handleNext">»</button>
                </div>
            </div>
        </div>
        <dialog id="my_modal_1" class="modal" ref="modal">
            <div class="modal-box">
                <form method="dialog">
                    <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
                </form>
                <h3 class="font-bold text-lg">{{ isAdd ? 'Add User' : 'Edit User' }}</h3>
                <label class="form-control w-full max-w-xs">
                    <div class="label">
                        <span class="label-text">Name</span>
                    </div>
                    <input name="name" type="text" placeholder="Please input user name"
                        class="input input-bordered w-full max-w-xs" v-model="formValue.name" />
                </label>
                <div class="form-control max-w-xs">
                    <div class="flex flex-row items-center">
                        <label class="label cursor-pointer mr-5">
                            <div class="label">
                                <span class="label-text">Male</span>
                            </div>
                            <input type="radio" name="gender" class="radio checked:bg-blue-500" value="male" v-model="formValue.gender" />
                        </label>
                        <label class="label cursor-pointer">
                            <div class="label">
                                <span class="label-text">Female</span>
                            </div>
                            <input type="radio" name="gender" class="radio checked:bg-red-500" value="female" v-model="formValue.gender" />
                        </label>
                    </div>
                </div>

                <div class="modal-action">
                    <button class="btn btn-active btn-secondary" @click="SubmitUserForm">{{ isAdd ? 'Add' : 'Edit' }}</button>
                    <form method="dialog">
                        <!-- if there is a button in form, it will close the modal -->
                        <button class="btn">Close</button>
                    </form>
                </div>
            </div>
        </dialog>
    </div>
</template>

<style scoped></style>
