using UnityEngine;

namespace Universe.Player
{
    public class MicrophoneInputDetector : MonoBehaviour
    {
        public string activeDevice;

        private void Start()
        {
            if (Microphone.devices.Length > 0)
            {
                activeDevice = Microphone.devices[0];
                Debug.Log($"Microphone detected: {activeDevice}");
            }
            else
            {
                Debug.LogWarning("No microphone found.");
            }
        }
    }
}
