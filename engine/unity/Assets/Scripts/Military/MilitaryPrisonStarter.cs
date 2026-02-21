using UnityEngine;

namespace Universe.Military
{
    public class MilitaryPrisonStarter : MonoBehaviour
    {
        public GameObject fencedCompound;
        public GameObject guardNpcPrefab;
        public Animator jailDoorAnimator;

        public void ToggleJailDoor(bool open)
        {
            jailDoorAnimator?.SetBool("Open", open);
        }
    }
}
