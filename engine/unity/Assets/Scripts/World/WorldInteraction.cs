using UnityEngine;

namespace Universe.World
{
    public class WorldInteraction : MonoBehaviour
    {
        public float pickupRange = 3f;
        public Transform handAnchor;
        private Rigidbody heldItem;

        private void Update()
        {
            if (Input.GetKeyDown(KeyCode.E)) TryPickup();
            if (Input.GetKeyDown(KeyCode.Q)) ThrowHeld();
        }

        private void TryPickup()
        {
            if (heldItem != null) return;
            if (!Physics.Raycast(transform.position, transform.forward, out RaycastHit hit, pickupRange)) return;

            Rigidbody rb = hit.collider.attachedRigidbody;
            if (rb == null) return;
            heldItem = rb;
            rb.isKinematic = true;
            rb.transform.SetParent(handAnchor);
            rb.transform.localPosition = Vector3.zero;
        }

        private void ThrowHeld()
        {
            if (heldItem == null) return;
            heldItem.transform.SetParent(null);
            heldItem.isKinematic = false;
            heldItem.AddForce(transform.forward * 8f, ForceMode.Impulse);
            heldItem = null;
        }
    }
}
