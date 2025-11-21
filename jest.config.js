/** @type {import('jest').Config} */
const config = {
  // Define o ambiente de teste para simular um navegador
  testEnvironment: 'jest-environment-jsdom',

  // O diretório onde os testes estão localizados
  roots: ['<rootDir>/tests/frontend'],

  // Arquivo que será executado antes de cada suíte de testes
  setupFilesAfterEnv: ['<rootDir>/tests/frontend/setup.js'],

  // Informa ao Jest para não tentar transpilar o código com Babel
  transform: {},
};

module.exports = config;
