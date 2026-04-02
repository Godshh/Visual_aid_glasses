import LibGenerateTestUserSig from './lib-generate-test-usersig.min.js'

// ⚠️ 仅用于开发调试，上线前需改为后端生成 userSig
const SDK_APP_ID  = 1600134850
const SECRET_KEY  = '080c80b28bc06ccaa31f27f00c8972269cc6dc9675de78f27514033039f43202'
const EXPIRE_TIME = 604800  // 7天

export function genUserSig(userId) {
  const generator = new LibGenerateTestUserSig(SDK_APP_ID, SECRET_KEY, EXPIRE_TIME)
  return {
    sdkAppId: SDK_APP_ID,
    userSig: generator.genTestUserSig(userId),
  }
}
