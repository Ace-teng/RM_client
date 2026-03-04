/**
 * 模块 C：不可靠功能开关配置
 * 用户可在设置中启用/禁用下列功能
 */
export interface UnreliableFeaturesConfig {
  perspective: boolean;        // C1. 透视
  aiDecision: boolean;         // C2. 辅助决策
  highlightLowHP: boolean;     // C3. 高亮残血目标
  enemyAmmoEconomy: boolean;   // C4. 对面剩余发弹量/经济
  aimPrediction: boolean;      // C5. 自瞄预测攻击位置
  surroundAwareness: boolean;  // C6. 全向感知提醒
  heroBlindAssist: boolean;    // C7. 英雄吊射黑屏辅助UI
}

export const defaultUnreliableFeatures: UnreliableFeaturesConfig = {
  perspective: false,
  aiDecision: false,
  highlightLowHP: false,
  enemyAmmoEconomy: false,
  aimPrediction: false,
  surroundAwareness: false,
  heroBlindAssist: false
};
