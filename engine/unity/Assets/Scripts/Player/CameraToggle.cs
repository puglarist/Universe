using UnityEngine;

namespace Universe.Player
{
    public class CameraToggle : MonoBehaviour
    {
        public Camera firstPersonCamera;
        public Camera thirdPersonCamera;

        private void Start() => SetMode(true);

        private void Update()
        {
            if (Input.GetKeyDown(KeyCode.V))
                SetMode(!firstPersonCamera.gameObject.activeSelf);
        }

        private void SetMode(bool firstPerson)
        {
            firstPersonCamera.gameObject.SetActive(firstPerson);
            thirdPersonCamera.gameObject.SetActive(!firstPerson);
        }
    }
}
