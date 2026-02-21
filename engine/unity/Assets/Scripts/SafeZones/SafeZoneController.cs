using UnityEngine;

namespace Universe.SafeZones
{
    public class SafeZoneController : MonoBehaviour
    {
        private void OnTriggerEnter(Collider other)
        {
            if (!other.CompareTag("Player")) return;
            Debug.Log("Player entered safe zone: combat disabled.");
        }

        private void OnTriggerExit(Collider other)
        {
            if (!other.CompareTag("Player")) return;
            Debug.Log("Player exited safe zone: combat enabled.");
        }
    }
}
