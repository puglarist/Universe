using UnityEngine;

namespace Universe.Space
{
    public class SpacePatchStarter : MonoBehaviour
    {
        public Material spaceSkybox;
        public GameObject spaceshipInterior;
        public Transform pilotSeat;
        public Transform[] crewSeats;

        public void EnableSpaceSkybox()
        {
            if (spaceSkybox != null)
                RenderSettings.skybox = spaceSkybox;
        }
    }
}
