using UnityEngine;

namespace Universe.Combat
{
    public class CombatStarter : MonoBehaviour
    {
        public Animator animator;
        public int maxHealth = 100;
        public int currentHealth;
        public bool knockedOut;

        private void Start() => currentHealth = maxHealth;

        private void Update()
        {
            if (Input.GetMouseButtonDown(0)) animator?.SetTrigger("Punch");
            if (Input.GetMouseButtonDown(1)) animator?.SetTrigger("Block");
        }

        public void TakeDamage(int amount)
        {
            if (knockedOut) return;
            currentHealth = Mathf.Max(0, currentHealth - amount);
            if (currentHealth == 0)
            {
                knockedOut = true;
                animator?.SetTrigger("Knockout");
            }
        }
    }
}
