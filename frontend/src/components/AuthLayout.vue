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
                <h2 class="auth-title">Crie uma conta ou faça login</h2>
                <AuthTabs />
                <slot />
            </div>
        </div>
    </div>
</template>

<style scoped>
.auth-page {
    position: fixed;
    inset: 0;
    z-index: 10;
    display: grid;
    grid-template-columns: 1fr 520px;
    background: var(--bg);
}

/* ---------- Lado esquerdo ---------- */
.auth-hero {
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
    padding: clamp(24px, 28vh, 280px) 24px 24px;
    overflow-y: auto;
}

.auth-box {
    width: 100%;
    max-width: 420px;
    margin: 0 auto;
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
}
</style>