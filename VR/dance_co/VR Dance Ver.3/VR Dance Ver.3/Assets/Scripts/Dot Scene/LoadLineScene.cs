using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class LoadLineScene : MonoBehaviour
{
    public GameObject Yellow, Blue, flat;
    public GameObject Hearts, half, ring;
    public GameObject nullParent;

    float time;
    public bool Save;
    bool timeFin, timeCor;
    bool loadScene;

    AroundCircle aroundCircle;
    Heart heart;

    private void Start()
    {
        aroundCircle = GameObject.Find("AroundCircleManager").GetComponent<AroundCircle>();
        heart = GameObject.Find("HeartManager").GetComponent<Heart>();

        timeFin = timeCor = Save = false;
        loadScene = false;
        time = 0;
    }

    private void Update()
    {
        if (heart.heartFinish)
        {
            if (!timeCor)
            {
                StartCoroutine(TimeChecker());
                timeCor = true;
            }
        }

        if(Save && !loadScene)
        { 
            for (int i = 0; i < 10; i++)
            {
                aroundCircle.sphereList[i].SetActive(false);
            }

            Yellow.transform.SetParent(nullParent.transform);
            Blue.transform.SetParent(nullParent.transform);
            flat.transform.SetParent(nullParent.transform);

            Hearts.transform.position = Vector3.MoveTowards(Hearts.transform.position,
                new Vector3(-2.7f, 3.76f, 2.536f), 1.0f * Time.deltaTime);
            Hearts.transform.rotation = Quaternion.Slerp(Hearts.transform.rotation,
                Quaternion.Euler(11.2f, -145.17f, 37.1f), 1.0f * Time.deltaTime);

            Blue.transform.position = Vector3.MoveTowards(Blue.transform.position,
                new Vector3(-1, 1, 1), 1.0f * Time.deltaTime);
            Blue.transform.rotation = Quaternion.Slerp(Blue.transform.rotation,
                Quaternion.Euler(0, 0, 0), 1.0f * Time.deltaTime);

            Yellow.transform.position = Vector3.MoveTowards(Yellow.transform.position,
                new Vector3(-3, 2.5f, 0), 1.0f * Time.deltaTime);
            Yellow.transform.rotation = Quaternion.Slerp(Yellow.transform.rotation,
                Quaternion.Euler(0, 0, 0), 1.0f * Time.deltaTime);

            flat.transform.position = Vector3.MoveTowards(flat.transform.position,
                new Vector3(0, 2.5f, -3), 1.0f * Time.deltaTime);
            flat.transform.rotation = Quaternion.Slerp(flat.transform.rotation,
                Quaternion.Euler(0, 0, 0), 1.0f * Time.deltaTime);

            ring.transform.position = Vector3.MoveTowards(ring.transform.position,
                new Vector3(3, 2.53f, 0), 1.0f * Time.deltaTime);
            ring.transform.rotation = Quaternion.Slerp(ring.transform.rotation,
                Quaternion.Euler(0, 0, 90), 1.0f * Time.deltaTime);

            half.transform.position = Vector3.MoveTowards(half.transform.position,
                new Vector3(0, 2.65f, 3), 1.0f * Time.deltaTime);
            half.transform.rotation = Quaternion.Slerp(half.transform.rotation,
                Quaternion.Euler(0, 0, 0), 1.0f * Time.deltaTime);

            if(Hearts.transform.position == new Vector3(-2.7f, 3.76f, 2.536f) &&
                Blue.transform.position == new Vector3(-1, 1, 1) &&
                Yellow.transform.position == new Vector3(-3, 2.5f, 0) &&
                flat.transform.position == new Vector3(0, 2.5f, -3) &&
                ring.transform.position == new Vector3(3,2.53f,0) &&
                half.transform.position == new Vector3(0, 2.65f,3))
            {
                Invoke("LTrue", 3.0f);
            }
        }

        if(loadScene)
        {
            SceneManager.LoadScene("User Line Scene");
        }
    }

    void LTrue()
    {
        loadScene = true;
    }

    IEnumerator TimeChecker()
    {
        while(!timeFin)
        {
            time += 0.1f;

            if(time >=5f) {
                Save = true;
                timeFin = true;
            }

            yield return new WaitForSeconds(0.1f);
        }
    }
}
