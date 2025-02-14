
<script setup lang="ts">

import InputMask from "primevue/inputmask";
import Button from 'primevue/button';
import Password from 'primevue/password'
import { useToast } from 'primevue/usetoast';

const form = ref({ phone: '', password: '' })
const toast = useToast();
const authStore = useAuthStore()
const router = useRouter()

async function login() {
  if (!form.value.phone || !form.value.password) {
    toast.add({ summary: "Ошибка", severity: "error", detail: "Вы не заполнили поля", life: 3000})
    return
  }
  const result = await authStore.login(form.value.phone, form.value.password)
  if(result.status != 200){
    toast.add({ summary: "Ошибка", severity: "error", detail: "Пользователь с таким телефоном и паролем не существует", life: 3000})
  } else {
    toast.add({ summary: "Удачно", severity: "success", detail: "Вы авторизовались", life: 3000})
    router.push({path: "/"})
  }
}

definePageMeta({
  title: 'login',
  need_not_auth: true
})


</script>

<template>
    <div class="login_page">
        <Header></Header>
        <div class="content_with_footer">
            <div class="content">
                <div class="login_form">
                    <div class="description">
                        <p>Вход</p>
                    </div>
                    <form class="form" @submit.prevent="SignIn">
                        <InputMask class="field_input" id="basic" v-model="form.phone" mask="+7 (999) 999-99-99"
                            placeholder="+7 (999) 999-99-99" />
                        <Password class="field_input" id="password" name="password" toggleMask placeholder="Пароль"
                            promptLabel="Введите пароль" weakLabel="Слабый пароль" mediumLabel="Обычный пароль"
                            strongLabel="Сильный пароль" type="password" v-model="form.password"></Password>
                        <Button class="field_input" id="go_button" label="Войти" @click="login"></Button>
                        <!-- <p v-if="incorrect_data" class="auth_error">
                            {{ error }}
                        </p> -->
                    </form>
                </div>
                <NuxtLink to="/auth/register" class="register">
                    <p>Зарегистрироваться </p>
                </NuxtLink>

            </div>
            <Footer class="footer"></Footer>
        </div>
    </div>
</template>

<style scoped>

</style>
