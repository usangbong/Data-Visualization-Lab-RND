using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;
using cakeslice;
namespace PieChart.ViitorCloud
{
    public class PartProperties : MonoBehaviour
    {
        public Vector3 forward;
        public GameObject MyDetailObject;
        bool animDetailObject;
        bool lerpYourself;
        Color color;
        public float speed = 1.19f;

        public Vector3 MyCurrntPosition;
        Material material;
        public void SetInit()
        {
            forward = transform.TransformPoint(GetMidPont(GetComponent<MeshCollider>()));
            forward = new Vector3(forward.x, forward.y, transform.position.z);
            if (gameObject.GetComponent<Outline>() == null)
                gameObject.AddComponent<Outline>();
            GetComponent<Outline>().enabled = false;
            //GameObject game = GameObject.CreatePrimitive(PrimitiveType.Cube);
            //game.transform.localScale = (Vector3.one) * 0.3f;
            //GameObject detailibj = Instantiate(game, forward, Quaternion.identity);
            //material = detailibj.GetComponent<MeshRenderer>().material;
            //material.color = GetComponent<MeshRenderer>().material.color;
            //Destroy(game);
        }

        public void SetAnimation(bool mat)
        {
            if (MyDetailObject == null)
                return;
            color = MyDetailObject.GetComponent<UnityEngine.UI.Image>().color;
            animDetailObject = mat;

            if (!mat)
            {
                color.a = 1;
                MyDetailObject.GetComponent<UnityEngine.UI.Image>().color = color;
            }
        }
        void Update()
        {
            if (animDetailObject)
            {
                color.a = Mathf.PingPong(Time.time * speed, 1);
                MyDetailObject.GetComponent<UnityEngine.UI.Image>().color = color;
            }
            if (lerpYourself)
            {

            }
        }
        public static Vector3 GetMidPont(MeshCollider m_Collider)
        {
            return Distinct(m_Collider.sharedMesh.vertices)[Distinct(m_Collider.sharedMesh.vertices).Length / 2];
            Vector3[] Distinct(Vector3[] handles) => handles.ToList().Distinct().ToArray();
        }
    }
}