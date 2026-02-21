using UnityEngine;

namespace Universe.Combat
{
    public class MmaModule : MonoBehaviour
    {
        [Range(0f, 100f)] public float stamina = 100f;
        public bool oneHandBehindBackMode;
        public Rigidbody targetRagdoll;

        public void Grapple()
        {
            stamina = Mathf.Max(0, stamina - 10f);
            Debug.Log("Grapple executed.");
        }

        public void Takedown(Vector3 force)
        {
            if (targetRagdoll != null)
                targetRagdoll.AddForce(force, ForceMode.Impulse);
            stamina = Mathf.Max(0, stamina - 15f);
        }
    }
}
