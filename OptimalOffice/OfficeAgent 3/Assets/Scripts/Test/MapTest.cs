using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MapTest : MonoBehaviour
{
    const int XSIZE = 2;
    const int ZSIZE = 4;

    public Transform bed, sofa;
    public Map map;

    void Start()
    {
        int x = Random.Range(0, 11);
        int z = Random.Range(-8, 1);

        bed.transform.position = new Vector3(x, 0, z);
        map.fillMap(x, z * -1, XSIZE, ZSIZE, Color.black);

        while (true)
        {
            x = Random.Range(0, 9);
            z = Random.Range(-10, 1);

            sofa.position = new Vector3(x, 0, z);

            if (map.canFillMap(x, z * -1, ZSIZE, XSIZE))
            {
                map.fillMap(x, z * -1, ZSIZE, XSIZE, Color.blue);
                break;
            }
        }
    }

    void Update()
    {
        int bx = (int)bed.position.x;
        int bz = (int)bed.position.z;

        int sx = (int)sofa.position.x;
        int sz = (int)sofa.position.z;

        map.deleteMap(bx, bz * -1, XSIZE, ZSIZE);

        if (Input.GetKeyDown(KeyCode.RightArrow))
        {
            if (map.canFillMap(bx + 1, bz*-1, XSIZE, ZSIZE))
            {
                bed.position = new Vector3(bed.position.x + 1, 0, bed.position.z);
            }

            else
            {
                Debug.Log("Cant");
            }
        }

        else if(Input.GetKeyDown(KeyCode.LeftArrow))
        {
            if (map.canFillMap(bx - 1, bz * -1, XSIZE, ZSIZE))
            {
                bed.position = new Vector3(bed.position.x - 1, 0, bed.position.z);
            }

            else
            {
                Debug.Log("Cant");
            }
        }

        else if(Input.GetKeyDown(KeyCode.UpArrow))
        {
            if(map.canFillMap(bx, (bz + 1) * -1, XSIZE, ZSIZE))
            {
                bed.position = new Vector3(bed.position.x, 0, bed.position.z + 1);
            }

            else
            {
                Debug.Log("Cant");
            }
        }

        else if(Input.GetKeyDown(KeyCode.DownArrow))
        {
            if(map.canFillMap(bx, (bz - 1) * -1, XSIZE, ZSIZE))
            {
                bed.position = new Vector3(bed.position.x, 0, bed.position.z - 1);
            }

            else
            {
                Debug.Log("Cant");
            }
        }

        map.fillMap(bx, bz * -1, XSIZE, ZSIZE, Color.black);

        map.deleteMap(sx, sz * -1, ZSIZE, XSIZE);

        if (Input.GetKeyDown(KeyCode.D))
        {
            if (map.canFillMap(sx + 1, sz * -1, ZSIZE, XSIZE))
            {
                sofa.position = new Vector3(sofa.position.x + 1, 0, sofa.position.z);
            }

            else
            {
                Debug.Log("Cant");
            }
        }

        else if(Input.GetKeyDown(KeyCode.A))
        {
            if (map.canFillMap(sx - 1, sz * -1, ZSIZE, XSIZE))
            {
                sofa.position = new Vector3(sofa.position.x - 1, 0, sofa.position.z);
            }

            else
            {
                Debug.Log("Cant");
            }
        }

        else if(Input.GetKeyDown(KeyCode.W))
        {
            if (map.canFillMap(sx, (sz + 1) * -1, ZSIZE, XSIZE))
            {
                sofa.position = new Vector3(sofa.position.x, 0, sofa.position.z + 1);
            }

            else
            {
                Debug.Log("Cant");
            }
        }

        else if(Input.GetKeyDown(KeyCode.S))
        {
            if (map.canFillMap(sx, (sz - 1) * -1, ZSIZE, XSIZE))
            {
                sofa.position = new Vector3(sofa.position.x, 0, sofa.position.z - 1);
            }

            else
            {
                Debug.Log("Cant");
            }
        }

        map.fillMap(sx, sz * -1, ZSIZE, XSIZE, Color.blue);
    }
}
