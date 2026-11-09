<script setup>
import AuthTabs from "./AuthTabs.vue";
</script>

<template>
    <div class="auth-page">
        <aside class="auth-hero">
            <div class="hero-content">
                <img src="/logo-white.svg" alt="Achados e Perdidos UFU" class="hero-logo" />
                <h1>Achados e Perdidos UFU</h1>
                <p>
                    Perdeu algo no campus? Achou um objeto sem dono?
                    Cadastre aqui e ajude a devolver cada coisa para quem procura.
                </p>
            </div>
        </aside>

        <div class="auth-side">
            <div class="auth-box">
                <div class="mobile-brand">
                    <img src="/logo.svg" alt="" />
                    <span>Achados e Perdidos UFU</span>
                </div>
                <h2 class="auth-title">Crie uma conta ou faça login</h2>
                <AuthTabs />
                <slot />
            </div>
        </div>
    </div>
</template>

<style scoped>
.auth-page {
    min-height: 100vh;
    min-height: 100dvh;
    display: grid;
    grid-template-columns: 1fr 520px;
    background: var(--bg);
}

/* ---------- Lado esquerdo ---------- */
.auth-hero {
    position: sticky;
    top: 0;
    height: 100vh;
    height: 100dvh;
    display: flex;
    align-items: center;
    padding: 48px;
    color: #fff;
    background: linear-gradient(135deg, #0f3fa8, #1f6feb);
}

.hero-content {
    max-width: 480px;
}

.hero-logo {
    display: block;
    width: 96px;
    height: 96px;
    margin-bottom: 24px;
}

.hero-content h1 {
    margin: 0 0 16px;
    font-size: clamp(2rem, 4vw, 3.25rem);
    line-height: 1.1;
}

.hero-content p {
    margin: 0;
    font-size: 1.125rem;
    line-height: 1.5;
    opacity: 0.9;
}

/* ---------- Lado direito ---------- */
.auth-side {
    display: flex;
    align-items: flex-start;
    padding: clamp(24px, 20vh, 220px) 24px 24px;
}

.auth-box {
    width: 100%;
    max-width: 420px;
    margin: 0 auto;
}

.mobile-brand {
    display: none;
}

.auth-title {
    margin: 0 0 16px;
    text-align: center;
    font-size: 1.25rem;
}

.auth-box :deep(.card) {
    min-height: 400px;
}

.auth-box :deep(.card h1) {
    margin: 8px 0 16px;
    font-size: 1.75rem;
}

/* ---------- Telas pequenas ---------- */
@media (max-width: 900px) {
    .auth-page {
        grid-template-columns: 1fr;
    }

    .auth-hero {
        display: none;
    }

    .auth-side {
        padding-top: 32px;
    }

    .mobile-brand {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        margin-bottom: 24px;
        font-weight: 700;
        font-size: 1.125rem;
    }

    .mobile-brand img {
        width: 40px;
        height: 40px;
    }
}
</style>